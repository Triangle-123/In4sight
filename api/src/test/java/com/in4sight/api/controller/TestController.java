package com.in4sight.api.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestAttribute;
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

	@GetMapping("/api/test/counseling")
	public SseEmitter connectSse(
		@RequestParam("task_id") String taskId
	) {
		return emitterService.getEmitter(taskId);
	}

	@PreAuthorize("@authExpression.matchIpByRegex(#ip, '^192\\.168\\..*\\..*$')")
	@GetMapping("/api/test/allow-private-ip")
	public ResponseEntity<String> allowPrivateIp(
		@RequestAttribute("CLIENT_IPV4")
		String ip
	) {
		return ResponseEntity.ok("Allow private IP");
	}

	@PreAuthorize("@authExpression.matchIpByRegex(#ip, '^$')")
	@GetMapping("/api/test/deny-all-ip")
	public ResponseEntity<String> denyAllIp(
		@RequestAttribute("CLIENT_IPV4")
		String ip
	) {
		return ResponseEntity.ok("Deny all IP");
	}

	@PreAuthorize("@authExpression.matchIpByAllowedList(#ip)")
	@GetMapping("/api/test/allow-list-ip")
	public ResponseEntity<String> allowListIp(
		@RequestAttribute("CLIENT_IPV4")
		String ip
	) {
		return ResponseEntity.ok("Allow list IP");
	}
}
