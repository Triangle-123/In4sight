package com.in4sight.api.service;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import com.fasterxml.jackson.databind.ObjectMapper;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.in4sight.api.domain.CustomerDevice;
import com.in4sight.api.domain.LogByCustomer;
import com.in4sight.api.dto.CounselingRequestDto;
import com.in4sight.api.dto.CustomerResponseDto;
import com.in4sight.api.dto.DeviceResponseDto;
import com.in4sight.api.dto.EventDataDto;
import com.in4sight.api.dto.EventDataResponseDto;
import com.in4sight.api.dto.SolutionDto;
import com.in4sight.api.dto.SolutionResponseDto;
import com.in4sight.api.dto.TimeSeriesDataDto;
import com.in4sight.api.dto.TimeSeriesDataResponseDto;
import com.in4sight.api.repository.CounselingRepository;
import com.in4sight.eda.producer.KafkaProducer;

@Slf4j
@Service
@AllArgsConstructor
public class EmitterService {

	private final ConcurrentHashMap<String, SseEmitter> emitters = new ConcurrentHashMap<>();
	private final DeviceService deviceService;
	private final CounselingRepository counselingRepository;
	private final KafkaProducer kafkaProducer;

	public SseEmitter addEmitter(String taskId, SseEmitter emitter) throws Exception {
		emitters.computeIfAbsent(taskId, key -> emitter);
		emitter.onCompletion(() -> emitters.remove(taskId));
		emitter.onTimeout(() -> emitters.remove(taskId));
		emitter.send("SSE connect");
		return emitter;
	}

	public SseEmitter getEmitter(String taskId) {
		return emitters.getOrDefault(taskId, null);
	}

	public void startProcess(String taskId, CustomerResponseDto customerResponseDto) throws Exception {
		SseEmitter emitter = emitters.get(taskId);
		if (emitter == null) {
			throw new NoSuchElementException("해당하는 taskId가 없습니다.");
		}
		CompletableFuture<Void> sendCustomerInfo = CompletableFuture.runAsync(() -> {
			try {
				SseEmitter.SseEventBuilder event = SseEmitter.event()
					.name("customer-info")
					.data(customerResponseDto);
				emitter.send(event);
			} catch (Exception e) {
				log.error(e.getMessage());
			}
		});

		CompletableFuture<Void> sendDevicesInfo = CompletableFuture.runAsync(() -> {
			try {
				SseEmitter.SseEventBuilder event = SseEmitter.event()
					.name("device-info")
					.data(deviceService.findDevice(customerResponseDto.getCustomerId()));
				emitter.send(event);
			} catch (Exception e) {
				log.error(e.getMessage());
			}
		});

		CompletableFuture<Void> sendCounsellingRequest = CompletableFuture.runAsync(() -> {
			counselingRepository.deleteAll();
			List<DeviceResponseDto> deviceResponse = deviceService.findDevice(customerResponseDto.getCustomerId());
			List<CustomerDevice> devices = new ArrayList<>();
			List<String> serialNumbers = new ArrayList<>();
			for (DeviceResponseDto device : deviceResponse) {
				devices.add(
					new CustomerDevice(
						device.getProductType(),
						device.getModelSuffix(),
						device.getSerialNumber(),
						new ArrayList<>()));
				serialNumbers.add(device.getSerialNumber());
			}
			counselingRepository.save(
				new LogByCustomer(
					customerResponseDto.getCustomerId(),
					LocalDate.now().format(DateTimeFormatter.ofPattern("YYYY-MM-dd")),
					devices));

			log.info("counseling request: {}", serialNumbers);
			kafkaProducer.broadcastEvent("counseling_request", new CounselingRequestDto(taskId, serialNumbers));
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
		} catch (Exception e) {
			log.error(e.getMessage());
		}
	}

	@KafkaListener(topics = "data_sensor", groupId = "#{appProperties.getConsumerGroup()}")
	public void sensorListener(LinkedHashMap messages) {
		try {
			log.info("sensor received");
//			log.info(messages);
			TimeSeriesDataDto data = new ObjectMapper().convertValue(messages, TimeSeriesDataDto.class);
			log.info(data.getTaskId(), data.getSerialNumber());
			sendEvent(data.getTaskId(), "sensor-data", TimeSeriesDataResponseDto.builder()
				.serialNumber(data.getSerialNumber())
				.sensorData(data.getSensorData())
				.build());
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
			sendEvent(data.getTaskId(), "event-data", EventDataResponseDto.builder()
				.serialNumber(data.getSerialNumber())
				.data(data.getData())
				.build());
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
			log.info(data.getTaskId(), data.getResult().getSerialNumber());
			sendEvent(data.getTaskId(), "solution", SolutionResponseDto.builder()
				.result(data.getResult())
				.build());
		} catch (Exception e) {
			log.error(e.getMessage());
		}
	}
}
