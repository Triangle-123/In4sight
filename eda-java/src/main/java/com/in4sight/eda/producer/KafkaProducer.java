package com.in4sight.eda.producer;

import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class KafkaProducer {
	private final KafkaTemplate<String, Object> kafkaTemplate;

	public KafkaProducer(KafkaTemplate<String, Object> kafkaTemplate) {
		this.kafkaTemplate = kafkaTemplate;
	}

	public void broadcastEvent(String topic, Object event) {
		kafkaTemplate.send(topic, event);
	}
}
