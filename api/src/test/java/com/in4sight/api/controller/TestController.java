package com.in4sight.api.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import com.in4sight.api.service.EmitterService;

@RestController
public class TestController {

	private final EmitterService emitterService;

	@Autowired
	public TestController(EmitterService emitterService) {
		this.emitterService = emitterService;
	}

	@GetMapping("/api/v1/counseling")
	public SseEmitter connectSse(
		@RequestParam("task_id") String taskId
	) {
		return emitterService.getEmitter(taskId);
	}
}
