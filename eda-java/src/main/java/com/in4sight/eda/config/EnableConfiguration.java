package com.in4sight.eda.config;

import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.context.annotation.Bean;

@AutoConfiguration
public class EnableConfiguration {
	@Bean
	public AppProperties appProperties() {
		return new AppProperties();
	}
}
