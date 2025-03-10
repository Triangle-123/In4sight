package com.in4sight.eda;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.test.context.EmbeddedKafka;
import org.springframework.test.annotation.DirtiesContext;

import com.in4sight.eda.producer.KafkaProducer;

@SpringBootTest
@DirtiesContext
@EmbeddedKafka(topics = { "test-topic" })
@DisplayName("카프카 테스트")
public class KafkaConsumerTests {
	private KafkaProducer kafkaProducer;

	@Autowired
	public void setKafkaProducer(KafkaProducer kafkaProducer) {
		this.kafkaProducer = kafkaProducer;
	}

	private final CountDownLatch latch = new CountDownLatch(1);
	private final String topicName = "test-topic";
	private final String groupId = "test-group";
	private TestPayload payload;


	@KafkaListener(topics = topicName, groupId = groupId)
	public void listener(TestPayload message) {
		this.payload = message;
		latch.countDown();
	}

	@Test
	@DisplayName("카프카 Produce Consume 통합 테스트")
	void test() throws InterruptedException {
		String testMessage = "test-message";
		TestPayload testPayload = new TestPayload();
		testPayload.setName(testMessage);
		kafkaProducer.broadcastEvent(topicName, testPayload);

		boolean messageConsumed = latch.await(10, TimeUnit.SECONDS);
		Assertions.assertTrue(messageConsumed);
		Assertions.assertEquals(testMessage, payload.getName());
	}

}
