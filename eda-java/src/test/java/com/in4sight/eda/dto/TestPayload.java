package com.in4sight.eda.dto;

import lombok.Data;

@Data
public class TestPayload {
	Child name;

	@Data
	public static class Child {
		private String child;
	}
}
