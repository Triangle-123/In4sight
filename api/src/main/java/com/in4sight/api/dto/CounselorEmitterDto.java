package com.in4sight.api.dto;


import org.springframework.http.ResponseCookie;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

public record CounselorEmitterDto(
	ResponseCookie taskCookie,
	SseEmitter sseEmitter
) { }
