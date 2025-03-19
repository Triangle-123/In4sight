package com.in4sight.api.domain;

import java.util.List;

import org.springframework.data.mongodb.core.mapping.Field;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
public class CustomerDevice {

	@Field("product_type")
	private final String productType;

	@Field("model_suffix")
	private final String modelSuffix;

	@Field("serial_number")
	private final String serialNumber;

	private List<Issue> issues;
}
