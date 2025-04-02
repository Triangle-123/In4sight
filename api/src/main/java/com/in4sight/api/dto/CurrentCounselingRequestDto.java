package com.in4sight.api.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
public class CurrentCounselingRequestDto {
	private int customerId;
	private String counselingDate;
}
