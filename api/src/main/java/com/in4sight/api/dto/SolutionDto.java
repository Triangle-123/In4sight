package com.in4sight.api.dto;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import com.in4sight.api.domain.Solution;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SolutionDto {

	private String taskId;

	@JsonProperty("customer_id")
	private int customerId;

	@JsonProperty("counseling_date")
	private String counselingDate;

	private Result result;

	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
	public static class Result {
		private String serialNumber;
		private TotalAnswer data;
	}

	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
	public static class TotalAnswer {
		private String failure;
		private List<String> cause;
		private List<String> sensor;
		private Solution solutions;
	}

	@Data
	@NoArgsConstructor
	@AllArgsConstructor
	@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
	public static class HistoricalContext {
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
