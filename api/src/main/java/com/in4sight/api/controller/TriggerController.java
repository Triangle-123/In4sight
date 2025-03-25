package com.in4sight.api.controller;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/trigger")
public class TriggerController {

	@PostMapping("")
	public void customerPhoneCall(
		@RequestBody
		String phoneNumber
	) {

	}

	@DeleteMapping("")
	public void endPhoneCall(
		@RequestBody
		String phoneNumber
	) {

	}
}
