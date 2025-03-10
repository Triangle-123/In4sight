package com.in4sight.eda.config;

import java.util.HashMap;
import java.util.Map;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.support.serializer.ErrorHandlingDeserializer;
import org.springframework.kafka.support.serializer.JsonDeserializer;

@Configuration
public class KafkaConsumerConfig {

	@Value("${kafka.host}")
	private String kafkaHost;

	@Value("${kafka.consume-group}")
	private String consumeGroup;

	@Bean
	public ConsumerFactory<String, Object> consumerFactory() {
		Map<String, Object> configs = new HashMap<>();
		configs.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaHost);
		configs.put(ConsumerConfig.GROUP_ID_CONFIG, consumeGroup);

		JsonDeserializer jsonDeserializer = new JsonDeserializer();
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
