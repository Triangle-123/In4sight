package com.in4sight.api.dto;

import java.time.LocalDate;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
@Builder
public class DeviceResponseDto {
	String serialNumber;
	String productType;
	String modelSuffix;
	String modelName;
	LocalDate launchDate;
}
