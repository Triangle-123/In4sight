package com.in4sight.api.domain;

import java.util.List;

import org.springframework.data.mongodb.core.mapping.Field;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
public class Issue {

	private String issue;

	@Field("issue_priority")
	private int issuePriority;

	private List<Solution> solutions;
}
