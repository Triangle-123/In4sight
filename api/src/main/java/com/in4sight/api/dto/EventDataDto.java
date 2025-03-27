package com.in4sight.api.dto;


import java.util.List;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class EventDataDto {
	private String taskId;
	private String serialNumber;

	private List<EventData> data;

	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
	public static class EventData {
		private String time;
		private String eventType;
		private String location;
	}
}
