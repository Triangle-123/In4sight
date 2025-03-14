package com.in4sight.api.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
@Builder
public class CustomerResponseDto {
	private int customerId;
	private String customerName;
	private String phoneNumber;
	private String address;
}
