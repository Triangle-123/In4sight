package com.in4sight.api.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.PathMatchConfigurer;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import com.in4sight.api.interceptor.IpInterceptor;

@Configuration
@EnableWebMvc
public class WebMvcConfig implements WebMvcConfigurer {
	@Value("${spring.application.version}")
	private String apiVersion;

	private final IpInterceptor ipInterceptor;

	@Autowired
	public WebMvcConfig(IpInterceptor ipInterceptor) {
		this.ipInterceptor = ipInterceptor;
	}

	@Override
	public void addInterceptors(InterceptorRegistry registry) {
		registry
			.addInterceptor(ipInterceptor)
			.addPathPatterns("/**");
	}

	@Override
	public void configurePathMatch(PathMatchConfigurer configurer) {
		configurer.addPathPrefix(
			String.format("/api/%s", apiVersion),
			(c) -> c.getPackageName().equals("com.in4sight.api.controller")
		);
	}
}
