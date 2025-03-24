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
public class TimeSeriesDataDto {

	private String taskId;
	private String serialNumber;
	private List<SensorData> data;

	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
	public static class SensorData {
		private String time;
		private String location;
		private String sensor;
		private Double value;
	}
}
