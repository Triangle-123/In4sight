package com.in4sight.api.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
@Builder
public class ModelSpecResponseDto {
	private String specGroup;
	private String specName;
	private String specValue;
}
