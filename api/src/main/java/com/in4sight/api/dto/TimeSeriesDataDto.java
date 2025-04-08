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
		private String measurement;
		private String icon;
		private String unit;

		private Criteria criteria;

		@JsonAlias("sensor_name")
		private String sensorName;

		private FieldData data;
	}

	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	public static class FieldData {
		private List<String> time;
		private List<Double> value;
	}

	@Data
	@NoArgsConstructor
	@AllArgsConstructor
	private static class Criteria {
		@JsonAlias("lower_limit")
		private int lowerLimit;

		@JsonAlias("upper_limit")
		private int upperLimit;

		private Threshold threshold;
	}

	@Data
	@NoArgsConstructor
	@AllArgsConstructor
	private static class Threshold {
		private ThresholdValue warning;
		private ThresholdValue critical;
	}

	@Data
	@NoArgsConstructor
	@AllArgsConstructor
	private static class ThresholdValue {
		private Double lower;
		private Double upper;
	}
}
