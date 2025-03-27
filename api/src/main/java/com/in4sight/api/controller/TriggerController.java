package com.in4sight.api.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Hidden;

import com.in4sight.api.dto.CustomerRequestDto;
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

	@PostMapping("")
	public void customerPhoneCall(
		@RequestBody
		String phoneNumber
	) {

	}

	/**
	 * 고객과 상담사의 연결 종료 요청
	 * @param customerRequestDto 연결 종료 고객의 정보
	 */
	@DeleteMapping("")
	public void endPhoneCall(
		@RequestBody
		CustomerRequestDto customerRequestDto
	) {
		customerService.disconnectCustomerAndCounselor(customerRequestDto);
	}
}
