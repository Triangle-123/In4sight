package com.in4sight.api.dto;

import java.util.List;

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
	ModelInfoResponseDto modelInfo;
	List<ModelSpecResponseDto> modelSpecs;
	List<ModelFeatureResponseDto> modelFeatures;
}
