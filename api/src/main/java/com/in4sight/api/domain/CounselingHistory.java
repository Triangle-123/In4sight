package com.in4sight.api.domain;

import java.util.List;

import org.springframework.data.mongodb.core.mapping.Field;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
public class CounselingHistory {
	@Field("counseling_date")
	private String counselingDate;

	@Field
	private List<CustomerDevice> devices;
}
