package com.in4sight.api.dto;

import org.springframework.data.mongodb.core.mapping.Field;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class PersonalizedSolution {

	@Field("personalized_context")
	private String personalizedContext;

	@Field("recommended_solution")
	private String recommendedSolution;

	@Field
	private String status;
}
