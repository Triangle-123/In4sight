package com.in4sight.api.service;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.in4sight.api.domain.CustomerDevice;
import com.in4sight.api.domain.LogByCustomer;
import com.in4sight.api.dto.CustomerResponseDto;
import com.in4sight.api.dto.DeviceResponseDto;
import com.in4sight.api.repository.CounsellingRepository;

@Slf4j
@Service
@AllArgsConstructor
public class EmitterService {

	private final ConcurrentHashMap<String, SseEmitter> emitters = new ConcurrentHashMap<>();
	private final DeviceService deviceService;
	private final CounsellingRepository counsellingRepository;
//	private final KafkaProducer kafkaProducer;

	public SseEmitter addEmitter(String taskId, SseEmitter emitter) throws Exception {
		emitters.put(taskId, emitter);
		emitter.onCompletion(() -> emitters.remove(taskId));
		emitter.onTimeout(() -> emitters.remove(taskId));
		emitter.send("SSE connect");
		return emitter;
	}

	public void startProcess(String taskId, CustomerResponseDto customerResponseDto) {
		SseEmitter emitter = emitters.get(taskId);

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
					.name("divice-info")
					.data(deviceService.findDevice(customerResponseDto.getCustomerId()));
				emitter.send(event);
			} catch (Exception e) {
				log.error(e.getMessage());
			}
		});

		CompletableFuture<Void> sendCounsellingRequest = CompletableFuture.runAsync(() -> {
			counsellingRepository.deleteAll();
			List<DeviceResponseDto> deviceResponse = deviceService.findDevice(customerResponseDto.getCustomerId());
			List<CustomerDevice> devices = new ArrayList<>();
			List<String> serialNumbers = new ArrayList<>();
			for(DeviceResponseDto device : deviceResponse) {
				devices.add(
					new CustomerDevice(
						device.getProductType(),
						device.getModelSuffix(),
						device.getSerialNumber(),
						new ArrayList<>()));
				serialNumbers.add(device.getSerialNumber());
			}
			counsellingRepository.save(
				new LogByCustomer(
					customerResponseDto.getCustomerId(),
					LocalDate.now().format(DateTimeFormatter.ofPattern("YYYY-MM-dd")),
					devices));
//			kafkaProducer.broadcastEvent("counsellingRequest", serialNumbers);

		});

		CompletableFuture.allOf(sendCustomerInfo, sendDevicesInfo, sendCounsellingRequest).join();
	}

//	@KafkaListener(topics = "", groupId = "consumer-java")
//	public void callback() {
//
//	}
}
