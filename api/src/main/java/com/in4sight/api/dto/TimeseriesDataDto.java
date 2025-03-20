package com.in4sight.api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


@Data
@NoArgsConstructor
@AllArgsConstructor
public class TimeseriesDataDto {
	private String time;
	private String location;
	private String sensor;
	private Double value;
}
