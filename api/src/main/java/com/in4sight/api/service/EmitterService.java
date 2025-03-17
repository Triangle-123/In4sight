package com.in4sight.api.service;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.in4sight.api.dto.CustomerResponseDto;

@Slf4j
@Service
@AllArgsConstructor
public class EmitterService {

	private final ConcurrentHashMap<String, SseEmitter> emitters = new ConcurrentHashMap<>();
	private final DeviceService deviceService;

	public SseEmitter addEmitter(String taskId, SseEmitter emitter) throws Exception {
		emitters.put(taskId, emitter);
		emitter.onCompletion(() -> emitters.remove(taskId));
		emitter.onTimeout(() -> emitters.remove(taskId));
		emitter.send("SSE connect");
		return emitter;
	}

	public void startProcess(String taskId, CustomerResponseDto customerResponseDto) throws Exception {
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

		CompletableFuture.allOf(sendCustomerInfo, sendDevicesInfo).join();
	}
}
