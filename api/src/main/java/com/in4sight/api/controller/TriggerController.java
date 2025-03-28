package com.in4sight.api.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Hidden;

import com.in4sight.api.service.CustomerService;

@Hidden
@RestController
@RequestMapping("/api/v1/trigger")
public class TriggerController {
	private final CustomerService customerService;

	@Autowired
	public TriggerController(final CustomerService customerService) {
		this.customerService = customerService;
	}

	/**
	 * 고객과 상담사의 연결 요청
	 * @param phoneNumber
	 */
	@PostMapping("")
	public void customerPhoneCall(
		@RequestBody
		String phoneNumber
	) {
		customerService.connectingCustomerAndCounselor(phoneNumber);
	}

	/**
	 * 고객과 상담사의 연결 종료 요청
	 * @param phoneNumber 연결 종료 고객의 전화번호
	 */
	@DeleteMapping("")
	public void endPhoneCall(
		@RequestBody
		String phoneNumber
	) {
		customerService.disconnectCustomerAndCounselor(phoneNumber);
	}
}
