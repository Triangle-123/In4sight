package com.in4sight.api.service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import org.springframework.http.ResponseCookie;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import com.fasterxml.jackson.databind.ObjectMapper;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.in4sight.api.domain.CustomerDevice;
import com.in4sight.api.dto.CounselingHistoryDto;
import com.in4sight.api.dto.CounselingRequestDto;
import com.in4sight.api.dto.CounselorEmitterDto;
import com.in4sight.api.dto.CustomerResponseDto;
import com.in4sight.api.dto.DeviceResponseDto;
import com.in4sight.api.dto.EventDataDto;
import com.in4sight.api.dto.EventDataResponseDto;
import com.in4sight.api.dto.SolutionDto;
import com.in4sight.api.dto.SolutionResponseDto;
import com.in4sight.api.dto.TimeSeriesDataDto;
import com.in4sight.api.dto.TimeSeriesDataResponseDto;
import com.in4sight.api.repository.CustomerEventCacheRepository;
import com.in4sight.api.util.CustomerCounselorMap;
import com.in4sight.eda.producer.KafkaProducer;

@Slf4j
@Service
@AllArgsConstructor
public class EmitterService {

	private final ConcurrentHashMap<String, SseEmitter> emitters = new ConcurrentHashMap<>();
	private final DeviceService deviceService;
	private final CounselingService counselingService;
	private final KafkaProducer kafkaProducer;
	private final CustomerCounselorMap customerCounselorMap;
	private final CustomerEventCacheRepository eventCacheRepository;

	public SseEmitter addEmitter(String taskId, SseEmitter emitter) throws Exception {
		emitters.computeIfAbsent(taskId, key -> emitter);
		emitter.onCompletion(() -> emitters.remove(taskId));
		emitter.onTimeout(() -> emitters.remove(taskId));

		String customerPhoneNumber = customerCounselorMap.getMappedCustomer(taskId);
		Map<String, Object> cache = eventCacheRepository.getCache(customerPhoneNumber);
		if (customerPhoneNumber == null || cache == null) {
			customerCounselorMap.setAvailableCounselor(taskId);
			emitter.send("SSE connect");
		} else {
			for (String key : cache.keySet()) {
				sendEvent(taskId, key, cache.get(key));
			}
		}
		sendHeartBeat(taskId);
		return emitter;
	}

	/**
	 * addEmitter overloading
	 * @return 상담사 연결 SseEmitter 및 Cookie 발급
	 */
	public CounselorEmitterDto addEmitter(String taskId) throws Exception {
		if (taskId == null || taskId.isEmpty()) {
			taskId = UUID.randomUUID().toString(); // 나중에 Task ID 생성 로직이 있다면 추가
		}

		// TaskId에 대한 쿠키 발급
		ResponseCookie taskCookie = ResponseCookie
			.from("task_id", taskId)
			.httpOnly(true)
			.path("/")
			.secure(true)
			.sameSite("None")
			.maxAge(TimeUnit.HOURS.toSeconds(8))
			.build();

		// TaskId에 맞는 SSE Emitter 생성
		SseEmitter emitter = emitters.get(taskId);
		if (emitter != null) {
			emitter.complete();
			emitters.remove(taskId);
		}
		emitter = new SseEmitter(TimeUnit.MINUTES.toMillis(10));
		emitter = addEmitter(taskId, emitter);

		return new CounselorEmitterDto(taskCookie, emitter);
	}

	public SseEmitter getEmitter(String taskId) {
		return emitters.getOrDefault(taskId, null);
	}

	public void sendHeartBeat(String taskId) {
		ScheduledExecutorService executor = Executors.newScheduledThreadPool(1);

		Runnable dropTheBeat = new Runnable() {
			@Override
			public void run() {
				try {
					SseEmitter emitter = getEmitter(taskId);
					if (emitter == null) {
						executor.shutdown();
					} else {
						log.info("send SSE HeartBeat : {}", taskId);
						emitter.send("SSE HeartBeat");
					}
				} catch (Exception e) {
					log.error(e.getMessage());
					executor.shutdown();
				}
			}
		};

		executor.scheduleWithFixedDelay(dropTheBeat, 0, 10, TimeUnit.SECONDS);
	}

	public Set<String> getAllCounselors() {
		return emitters.keySet();
	}

	public void startProcess(String taskId, CustomerResponseDto customerResponseDto) throws Exception {
		SseEmitter emitter = emitters.get(taskId);
		if (emitter == null) {
			throw new NoSuchElementException("해당하는 taskId가 없습니다.");
		}
		CompletableFuture<Void> sendCustomerInfo = CompletableFuture.runAsync(() -> sendEvent(
				taskId,
				"customer-info",
				customerResponseDto,
				true
			)
		);

		CompletableFuture<Void> sendDevicesInfo = CompletableFuture.runAsync(() -> sendEvent(
				taskId,
				"device-info",
				deviceService.findDevice(customerResponseDto.getCustomerId()),
				true
			)
		);
		CompletableFuture<Void> sendCounsellingRequest = CompletableFuture.runAsync(() -> {
			List<DeviceResponseDto> deviceResponse = deviceService.findDevice(customerResponseDto.getCustomerId());
			List<CustomerDevice> devices = new ArrayList<>();
			List<String> serialNumbers = new ArrayList<>();
			for (DeviceResponseDto device : deviceResponse) {
				devices.add(CustomerDevice.builder()
					.serialNumber(device.getSerialNumber())
					.build());
				serialNumbers.add(device.getSerialNumber());
			}
			log.info("counseling request: {}", serialNumbers);
			String counselingDate = LocalDateTime.now().format(DateTimeFormatter.ofPattern("YYYY-MM-dd HH:mm"));
			kafkaProducer.broadcastEvent("counseling_request",
				new CounselingRequestDto(taskId, serialNumbers));
			CounselingHistoryDto history = new CounselingHistoryDto(taskId,
				customerResponseDto.getCustomerId(),
				counselingDate,
				counselingService.findLog(customerResponseDto.getCustomerId()));
			kafkaProducer.broadcastEvent("counseling_history", history);
			log.info("send counselingHistory : {}", history);
			counselingService.addLog(customerResponseDto.getCustomerId(),
				counselingDate,
				devices);
		});

		CompletableFuture.allOf(sendCustomerInfo, sendDevicesInfo, sendCounsellingRequest).join();
	}

	/**
	 * SSE 이벤트 보내는 메서드
	 * @param taskId SSE Emitter TaskID
	 * @param eventName 전달한 이벤트 대분류
	 * @param eventDataDto 이벤트 데이터
	 * @param <E> 이벤트 자료구조
	 */
	public <E> void sendEvent(String taskId, String eventName, E eventDataDto) {
		try {
			SseEmitter emitter = getEmitter(taskId);
			SseEmitter.SseEventBuilder event = SseEmitter.event()
				.name(eventName)
				.data(eventDataDto);
			emitter.send(event);
			log.info("send " + eventName);
		} catch (Exception e) {
			log.error("failed to send " + eventName, e);
		}
	}

	/**
	 * SSE 이벤트 보내는 메서드 OverLoading
	 * @param taskId SSE Emitter TaskID
	 * @param eventName 전달한 이벤트 대분류
	 * @param eventDataDto 이벤트 데이터
	 * @param cache 캐시 여부 -> true 시 Cache에 데이터 저장
	 * @param <E> 이벤트 자료구조
	 */
	public <E> void sendEvent(String taskId, String eventName, E eventDataDto, boolean cache) {
		if (cache) {
			String customerPhoneNumber = customerCounselorMap.getMappedCustomer(taskId);
			eventCacheRepository.addCache(customerPhoneNumber, eventName, eventDataDto);
		}
		sendEvent(taskId, eventName, eventDataDto);
	}

	@KafkaListener(topics = "data_sensor", groupId = "#{appProperties.getConsumerGroup()}")
	public void sensorListener(LinkedHashMap messages) {
		try {
			log.info("sensor received");
			TimeSeriesDataDto data = new ObjectMapper().convertValue(messages, TimeSeriesDataDto.class);
			log.info(data.getTaskId(), data.getSerialNumber());
			sendEvent(
				data.getTaskId(),
				"sensor-data",
				TimeSeriesDataResponseDto.builder()
					.serialNumber(data.getSerialNumber())
					.sensorData(data.getSensorData())
					.build(),
				true
			);
		} catch (Exception e) {
			log.error(e.getMessage());
		}

	}

	@KafkaListener(topics = "data_event", groupId = "#{appProperties.getConsumerGroup()}")
	public void eventListener(LinkedHashMap messages) {
		try {
			log.info("event received");
			EventDataDto data = new ObjectMapper().convertValue(messages, EventDataDto.class);
			log.info(data.getTaskId(), data.getSerialNumber());
			sendEvent(
				data.getTaskId(),
				"event-data",
				EventDataResponseDto.builder()
					.serialNumber(data.getSerialNumber())
					.eventData(data.getEventData())
					.build(),
				true
			);
		} catch (Exception e) {
			log.error(e.getMessage());
		}
	}

	@KafkaListener(topics = "rag-result", groupId = "#{appProperties.getConsumerGroup()}")
	public void solutionListener(LinkedHashMap messages) {
		try {
			log.info("result received");
			log.info(messages.toString());
			SolutionDto data = new ObjectMapper().convertValue(messages, SolutionDto.class);
			SolutionDto.Result result = data.getResult();
			log.info(data.getTaskId(), result.getSerialNumber());
			counselingService.replaceLogByDevice(
				data.getCustomerId(),
				data.getCounselingDate(),
				CustomerDevice.builder()
					.serialNumber(result.getSerialNumber())
					.cause(result.getData().getCause())
					.failure(result.getData().getFailure())
					.sensor(result.getData().getSensor())
					.solutions(result.getData().getSolutions())
					.build());
			sendEvent(
				data.getTaskId(),
				"solution",
				SolutionResponseDto.builder()
					.result(data.getResult())
					.build(),
				true
			);
		} catch (Exception e) {
			log.error(e.getMessage());
		}
	}
}
