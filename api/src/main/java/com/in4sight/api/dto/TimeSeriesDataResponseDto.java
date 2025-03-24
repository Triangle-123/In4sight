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
public class TimeSeriesDataResponseDto {
	private String serialNumber;
	private List<TimeSeriesDataDto.SensorData> data;
}
