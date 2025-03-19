package com.in4sight.eda.config;

import java.util.HashMap;
import java.util.Map;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.support.serializer.ErrorHandlingDeserializer;
import org.springframework.kafka.support.serializer.JsonDeserializer;

@AutoConfiguration
public class KafkaConsumerConfig {
	private final AppProperties appProperties;

	@Autowired
	public KafkaConsumerConfig(AppProperties appProperties) {
		this.appProperties = appProperties;
	}

	@Bean
	public ConsumerFactory<String, Object> consumerFactory() {
		Map<String, Object> configs = new HashMap<>();
		configs.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, appProperties.getBootstrapServer());
		configs.put(ConsumerConfig.GROUP_ID_CONFIG, appProperties.getConsumerGroup());
		configs.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, 30000);
		configs.put(ConsumerConfig.HEARTBEAT_INTERVAL_MS_CONFIG, 1000);

		JsonDeserializer jsonDeserializer = new CustomJsonDeserializer(Object.class);
		jsonDeserializer.trustedPackages("*");

		ErrorHandlingDeserializer<Object> errorHandlingDeserializer =
			new ErrorHandlingDeserializer<>(jsonDeserializer);

		return new DefaultKafkaConsumerFactory<>(
			configs,
			new StringDeserializer(),
			errorHandlingDeserializer
		);
	}

	@Bean
	public ConcurrentKafkaListenerContainerFactory<String, String> kafkaListenerContainerFactory() {
		ConcurrentKafkaListenerContainerFactory<String, String> factory =
			new ConcurrentKafkaListenerContainerFactory<>();
		factory.setConsumerFactory(consumerFactory());
		return factory;
	}
}
