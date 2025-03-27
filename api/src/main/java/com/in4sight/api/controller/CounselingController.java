package com.in4sight.api.controller;

import java.util.NoSuchElementException;

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.Parameters;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.in4sight.api.dto.CounselorEmitterDto;
import com.in4sight.api.dto.CustomerRequestDto;
import com.in4sight.api.service.CustomerService;
import com.in4sight.api.service.EmitterService;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/counseling")
@CrossOrigin(origins = "*", allowedHeaders = "*")
@Slf4j
@Tag(name = "counselling", description = "counselling SSE API")
public class CounselingController {

	private final CustomerService customerService;
	private final EmitterService emitterService;

	@GetMapping(produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	@Operation(summary = "SSE 연결", description = "EventSource 객체를 통한 SSE 연결")
	public ResponseEntity<SseEmitter> counselorConnect(
		@CookieValue(value = "task_id", required = false)
		String taskId
	) throws Exception {
		CounselorEmitterDto counselorEmitter = emitterService.addEmitter(taskId);

		return ResponseEntity.ok()
			.header(HttpHeaders.SET_COOKIE, counselorEmitter.taskCookie().toString())
			.body(counselorEmitter.sseEmitter());
	}

	@GetMapping(value = "/{taskId}", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	@Operation(summary = "SSE 연결", description = "EventSource 객체를 통한 SSE 연결")
	public SseEmitter getEmitter(@PathVariable String taskId) {
		try {
			return emitterService.addEmitter(taskId, new SseEmitter(60L * 1000L * 10L));
		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}

	@PostMapping("/{taskId}")
	@Operation(summary = "상담 시작", description = "고객 정보로 상담 시작, SSE 이벤트를 통해 데이터 전송")
	@Parameters({
		@Parameter(name = "customerName", description = "고객명"),
		@Parameter(name = "phoneNumber", description = "고객 전화번호")
	})
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
			log.error(e.getMessage());
			return ResponseEntity.badRequest().body(e.getMessage());
		} catch (Exception e) {
			log.error(e.getMessage());
			return ResponseEntity.internalServerError().body("SSE 통신 중 에러 발생");
		}
	}
}
