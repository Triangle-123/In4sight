package com.in4sight.api.domain;

import org.springframework.data.mongodb.core.mapping.Field;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
public class Solution {

	private String solution;

	@Field("solution_priority")
	private int solutionPriority;
}
