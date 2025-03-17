package com.in4sight.api.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
public class CustomerRequestDto {
	private String customerName;
	private String phoneNumber;
}
