package com.in4sight.api.dto;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
public class CounselingRequestDto {
	private String taskId;
	private List<String> serialNumbers;
}
