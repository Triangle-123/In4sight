package com.in4sight.api.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
@Builder
public class ModelInfoResponseDto {
	private String modelSuffix;
	private String modelName;
	private String productType;
	private String purchaseDate;
	private String modelImage;
}
