package com.in4sight.api.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

import com.in4sight.api.domain.LogByCustomer;

@Getter
@AllArgsConstructor
@ToString
public class CounselingHistoryDto {
	private String taskId;
	private int customerId;
	private String counselingDate;

	private LogByCustomer histories;
}
