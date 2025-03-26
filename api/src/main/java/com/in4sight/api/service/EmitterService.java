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

	@KafkaListener(topics = "data_sensor", groupId = "#{appProperties.getConsumerGroup()}")
	public void sensorListener(String messages) throws Exception {
		log.info("sensor received");

		TimeSeriesDataDto data = new ObjectMapper().readValue(messages, TimeSeriesDataDto.class);
		log.info(data.getTaskId(), data.getSerialNumber());
		SseEmitter emitter = emitters.get(data.getTaskId());
		SseEmitter.SseEventBuilder event = SseEmitter.event()
			.name("sensor-data")
			.data(TimeSeriesDataResponseDto.builder()
				.serialNumber(data.getSerialNumber())
				.sensorData(data.getSensorData())
				.build());
		emitter.send(event);

	}

	@KafkaListener(topics = "data_event", groupId = "#{appProperties.getConsumerGroup()}")
	public void eventListener(String messages) throws Exception {

		log.info("event received");
		EventDataDto data = new ObjectMapper().readValue(messages, EventDataDto.class);
		log.info(data.getTaskId(), data.getSerialNumber());
		SseEmitter emitter = emitters.get(data.getTaskId());
		SseEmitter.SseEventBuilder event = SseEmitter.event()
			.name("event-data")
			.data(EventDataResponseDto.builder()
				.serialNumber(data.getSerialNumber())
				.data(data.getData())
				.build());
		emitter.send(event);
	}

	@KafkaListener(topics = "rag-result", groupId = "#{appProperties.getConsumerGroup()}")
	public void solutionListener(LinkedHashMap messages) throws Exception {
		log.info("result received");
		log.info(messages.toString());
//		SolutionDto data = new ObjectMapper().readValue(messages, SolutionDto.class);
//		SseEmitter emitter = emitters.get(data.getTaskId());
//		SseEmitter.SseEventBuilder event = SseEmitter.event()
//			.name("solution")
//			.data(data.getResult());
//		emitter.send(event);
	}
}
