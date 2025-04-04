package com.in4sight.api.domain;

import java.util.List;

import org.springframework.data.annotation.Transient;
import org.springframework.data.mongodb.core.mapping.Field;

import com.fasterxml.jackson.annotation.JsonAlias;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import com.in4sight.api.dto.PersonalizedSolution;
import com.in4sight.api.dto.SolutionDto;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ToString
public class Solution {

	@Transient
	@JsonAlias("historical_context")
	private SolutionDto.HistoricalContext historicalContext;

	@JsonAlias("personalized_solution")
	@Field("personalized_solution")
	private List<PersonalizedSolution> personalizedSolution;

	@JsonAlias("preventative_advice")
	@Field("preventative_advice")
	private List<String> preventativeAdvice;

}
