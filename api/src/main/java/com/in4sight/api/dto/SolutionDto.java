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
public class SolutionDto {

	private String taskId;
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
	private static class TotalAnswer {
		private String failure;
		private List<String> cause;
		private List<String> sensor;
		private Solution solutions;
	}

	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
	private static class Solution {
		private HistoricalContext historicalContext;
		private List<PersonalizedSolution> personalizedSolution;
		private List<String> preventativeAdvice;
	}

	@Data
	@NoArgsConstructor
	@AllArgsConstructor
	@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
	private static class HistoricalContext {
		private List<PreviousIssue> previousIssues;
	}

	@Data
	@NoArgsConstructor
	@AllArgsConstructor
	private static class PreviousIssue {
		private String cause;
		private String date;
		private String issue;
		private boolean resolved;
	}
}
