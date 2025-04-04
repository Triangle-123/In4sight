package com.in4sight.api.dto;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonAlias;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


@Data
@NoArgsConstructor
@AllArgsConstructor
public class TimeSeriesDataDto {

	private String taskId;
	private String serialNumber;

	@JsonAlias("sensor_data")
	private List<SensorData> sensorData;


	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	public static class SensorData {
		private String title;
		private String icon;
		private String unit;

		@JsonAlias("lower_bound")
		private int lowerBound;

		@JsonAlias("upper_bound")
		private int upperBound;

		@JsonAlias("warning_threshold")
		private int warningThreshold;

		@JsonAlias("danger_threshold")
		private int dangerThreshold;

		private boolean normal;
		private List<FieldData> data;
	}

	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	public static class FieldData {
		private String time;
		private Double value;
		private int status;
	}
}
