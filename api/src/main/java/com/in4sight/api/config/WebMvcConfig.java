package com.in4sight.api.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import com.in4sight.api.interceptor.IpInterceptor;

@Configuration
@EnableWebMvc
public class WebMvcConfig implements WebMvcConfigurer {
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
}
