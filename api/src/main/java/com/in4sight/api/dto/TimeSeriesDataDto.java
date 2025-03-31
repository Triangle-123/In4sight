package com.in4sight.api.dto;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;
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

	@JsonProperty("sensor_data")
	private List<SensorData> sensorData;


	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	public static class SensorData {
		private String title;
		private String icon;
		private String unit;

		@JsonProperty("is_abnormal")
		private boolean abnormal;

		private List<FieldData> data;
	}

	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
	public static class FieldData {
		private String time;
		private Double value;
	}
}
