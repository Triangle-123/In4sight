package com.in4sight.api.dto;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;


@Data
@NoArgsConstructor
@AllArgsConstructor
@ToString
@Builder
public class EventDataResponseDto {
	private String serialNumber;
	private List<EventDataDto.EventData> data;
}
