package com.in4sight.api.dto;


import java.util.List;

import com.fasterxml.jackson.annotation.JsonAlias;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class EventDataDto {
	private String taskId;
	private String serialNumber;

	@JsonAlias("event_data")
	private List<EventData> eventData;

	@Data
	@NoArgsConstructor
	@AllArgsConstructor
	public static class EventData {
		private String field;
		private String measurement;
		private List<String> time;
	}
}
