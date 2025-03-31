package com.in4sight.api.dto;


import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class EventDataDto {
	private String taskId;
	private String serialNumber;

	@JsonProperty("event_data")
	private List<String> eventData;
}
