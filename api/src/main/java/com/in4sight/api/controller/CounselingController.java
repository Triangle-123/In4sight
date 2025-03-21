package com.in4sight.api.controller;

import java.util.NoSuchElementException;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import lombok.AllArgsConstructor;

import com.in4sight.api.dto.CustomerRequestDto;
import com.in4sight.api.service.CustomerService;
import com.in4sight.api.service.EmitterService;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/counseling")
@CrossOrigin(origins = "*", allowedHeaders = "*")
public class CounselingController {

	private final CustomerService customerService;
	private final EmitterService emitterService;

	@GetMapping(value = "/{taskId}", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	public SseEmitter getEmitter(@PathVariable String taskId) {
		try {
			return emitterService.addEmitter(taskId, new SseEmitter(60L * 1000L * 10L));
		} catch (Exception e) {
			throw new RuntimeException(e);
		}

	}

	@PostMapping("/{taskId}")
	public ResponseEntity<?> startCounselling(
		@PathVariable
		String taskId,
		@RequestBody
		CustomerRequestDto customerRequestDto
	) {
		try {
			emitterService.startProcess(taskId, customerService.findCustomer(customerRequestDto));
			return ResponseEntity.ok().body("솔루션 요청 성공");
		} catch (NoSuchElementException e) {
			return ResponseEntity.badRequest().body(e.getMessage());
		} catch (Exception e) {
			return ResponseEntity.internalServerError().body("SSE 통신 중 에러 발생");
		}
	}
}
