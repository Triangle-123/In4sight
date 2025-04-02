package com.in4sight.api.domain;

import java.util.List;

import org.springframework.data.mongodb.core.mapping.Field;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

import com.in4sight.api.dto.PersonalizedSolution;

@Getter
@AllArgsConstructor
@ToString
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class Solution {

	@Field("personalized_solution")
	private List<PersonalizedSolution> personalizedSolution;

	@Field("preventative_advice")
	private List<String> preventativeAdvice;

}
