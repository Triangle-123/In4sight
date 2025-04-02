package com.in4sight.api.domain;

import java.util.List;

import org.springframework.data.annotation.Transient;
import org.springframework.data.mongodb.core.mapping.Field;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.ToString;

import com.in4sight.api.dto.PersonalizedSolution;
import com.in4sight.api.dto.SolutionDto;

@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ToString
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class Solution {

	@Transient
	private SolutionDto.HistoricalContext historicalContext;

	@Field("personalized_solution")
	private List<PersonalizedSolution> personalizedSolution;

	@Field("preventative_advice")
	private List<String> preventativeAdvice;

}
