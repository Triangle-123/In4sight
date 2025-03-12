package com.in4sight.eda.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@ConfigurationProperties(prefix = "eda.kafka")
public class AppProperties {
	private String bootstrapServer;
	private String consumerGroup;
}
