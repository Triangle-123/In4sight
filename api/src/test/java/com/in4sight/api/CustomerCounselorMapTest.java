package com.in4sight.api;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import jdk.jfr.Description;

import com.in4sight.api.service.EmitterService;
import com.in4sight.api.uttil.CustomerCounselorMap;


@DisplayName("고객과 상담사 매칭 자료구조 테스트")
@SpringBootTest
public class CustomerCounselorMapTest {
	private final CustomerCounselorMap customerCounselorMap;

	private static final String TASK_ID = "test";
	private static final int COUNSELOR_COUNT = 200;
	private static final int CUSTOMER_COUNT = 300;


	@MockitoBean
	private EmitterService emitterService;

	@Autowired
	public CustomerCounselorMapTest(CustomerCounselorMap customerCounselorMap) {
		this.customerCounselorMap = customerCounselorMap;
	}

	@DisplayName("상담 가능한 상담사의 Queue 테스트")
	@Description("상담사보다 많은 고객이 동시에 요청시 차이만큼은 TaskId을 응답받지 못함")
	@Test
	public void availableCounselorTest() throws InterruptedException {
		for (int i = 1; i <= COUNSELOR_COUNT; i++) {
			customerCounselorMap.setAvailableCounselor(TASK_ID + i);
			Mockito.when(emitterService.getEmitter(TASK_ID + i)).thenReturn(new SseEmitter());
		}

		CountDownLatch countDownLatch = new CountDownLatch(CUSTOMER_COUNT);
		AtomicInteger count = new AtomicInteger(0);
		Set<String> taskSet = new HashSet<>();

		try (ExecutorService executorService = Executors.newVirtualThreadPerTaskExecutor()) {
			for (int i = 0; i < CUSTOMER_COUNT; i++) {
				executorService.execute(() -> {
					String taskId = customerCounselorMap.getAvailableCounselorTaskId();
					if (taskId == null) {
						count.incrementAndGet();
					} else {
						taskSet.add(taskId);
					}
					countDownLatch.countDown();
				});
			}

			countDownLatch.await();

			Assertions.assertEquals(CUSTOMER_COUNT - COUNSELOR_COUNT, count.get());
			Assertions.assertEquals(COUNSELOR_COUNT, taskSet.size());
		}
	}


	@DisplayName("상담 연결된 고객 맵 테스트")
	@Description("여러명의 고객이 한번에 한명의 상담사에게 연결을 최초 연결 시도 한명만 성공")
	@Test
	public void customerMapTest() throws InterruptedException {
		CountDownLatch countDownLatch = new CountDownLatch(CUSTOMER_COUNT);
		AtomicInteger count = new AtomicInteger(0);
		String firstCustomerId = "";

		try (ExecutorService executorService = Executors.newVirtualThreadPerTaskExecutor()) {
			for (int i = 0; i < CUSTOMER_COUNT; i++) {
				String customerId = UUID.randomUUID().toString();
				if (i == 0) {
					firstCustomerId = customerId;
				}
				executorService.execute(() -> {
					try {
						customerCounselorMap.mappingCustomerAndCounselor(customerId, TASK_ID);
					} catch (Exception e) {
						count.incrementAndGet();
					}

					countDownLatch.countDown();
				});
				if (i == 0) {
					Thread.sleep(100);
				}
			}
		}

		countDownLatch.await();

		Assertions.assertEquals(CUSTOMER_COUNT - 1, count.get());
		Assertions.assertEquals(TASK_ID, customerCounselorMap.removeCustomer(firstCustomerId));
	}
}
