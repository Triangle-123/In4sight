package com.in4sight.api.domain;

import java.util.List;

import org.springframework.data.mongodb.core.mapping.Field;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder(toBuilder = true)
@ToString
public class CustomerDevice {

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
