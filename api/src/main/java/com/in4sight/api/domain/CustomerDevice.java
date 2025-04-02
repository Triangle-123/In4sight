package com.in4sight.api.domain;

import java.util.List;

import org.springframework.data.mongodb.core.mapping.Field;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@Builder(toBuilder = true)
@ToString
public class CustomerDevice {

//	@Field("product_type")
//	private String productType;
//
//	@Field("model_suffix")
//	private String modelSuffix;

	@Field("serial_number")
	private String serialNumber;

	@Field
	private List<String> cause;

	@Field
	private String failure;

	@Field
	private List<String> sensor;

	@Field
	private Solution solutions;

}
