package com.in4sight.eda.config;

import java.io.IOException;

import org.springframework.kafka.support.serializer.JsonDeserializer;

import com.fasterxml.jackson.databind.ObjectMapper;

public class CustomJsonDeserializer<T> extends JsonDeserializer<T> {

	private final ObjectMapper objectMapper = new ObjectMapper();
	private final Class<T> targetType;

	public CustomJsonDeserializer(Class<T> targetType) {
		super(targetType);
		this.targetType = targetType;
	}

	@Override
	public T deserialize(String topic, byte[] data) {
		if (data == null) {
			return null;
		}
		try {
			return objectMapper.readValue(data, targetType);
		} catch (IOException e) {
			throw new RuntimeException("Error deserializing JSON", e);
		}
	}
}
