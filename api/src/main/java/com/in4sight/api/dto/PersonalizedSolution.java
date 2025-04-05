package com.in4sight.api.dto;

import org.springframework.data.mongodb.core.mapping.Field;

import com.fasterxml.jackson.annotation.JsonAlias;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PersonalizedSolution {

	@Field("personalized_context")
	@JsonAlias("personalized_context")
	private String personalizedContext;

	@Field("recommended_solution")
	@JsonAlias("recommended_solution")
	private String recommendedSolution;

	@Field
	private String status;
}
