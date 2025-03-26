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
	private List<Result> result;

	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	@JsonNaming
	private static class Result {
		private String serialNumber;
		private List<SolutionDto.Data> data;
	}

	@lombok.Data
	@NoArgsConstructor
	@AllArgsConstructor
	@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
	private static class Data {
		private String status;
		private String issue;
		private String recommendedSolution;
	}


}
