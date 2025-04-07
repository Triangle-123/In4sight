package com.in4sight.api.dto;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonAlias;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import com.in4sight.api.domain.Solution;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SolutionDto {

	private String taskId;

	@JsonAlias("customer_id")
	private int customerId;

	@JsonAlias("counseling_date")
	private String counselingDate;

	private Result result;

	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	public static class Result {

		@JsonAlias("serial_number")
		private String serialNumber;
		private TotalAnswer data;
	}

	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	public static class TotalAnswer {
		private String failure;
		private List<String> cause;

		@JsonAlias("related_sensor_en")
		private List<String> relatedSensorEn;

		private List<String> sensor;
		private Solution solutions;
	}

	@Data
	@NoArgsConstructor
	@AllArgsConstructor
	public static class HistoricalContext {
		@JsonAlias("previous_issues")
		private List<PreviousIssue> previousIssues;
	}

	@Data
	@NoArgsConstructor
	@AllArgsConstructor
	public static class PreviousIssue {
		private String cause;
		private String date;
		private String issue;
		private boolean resolved;
	}
}
