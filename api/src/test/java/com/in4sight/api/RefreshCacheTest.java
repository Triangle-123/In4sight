package com.in4sight.api;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseCookie;

import jdk.jfr.Description;

import com.in4sight.api.service.EmitterService;
import com.in4sight.api.util.CustomerCounselorMap;

@DisplayName("캐싱 데이터 테스트")
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class RefreshCacheTest {
	@LocalServerPort
	private int port;

	private final EmitterService emitterService;
	private final CustomerCounselorMap customerCounselorMap;

	private static final String EVENT_NAME = "eventName";
	private static final String EVENT_DATA = "eventData";
	private static final String CUSTOMER_PHONE_NUMBER = "phoneNumber";

	@Autowired
	public RefreshCacheTest(
		EmitterService emitterService,
		CustomerCounselorMap customerCounselorMap
	) {
		this.emitterService = emitterService;
		this.customerCounselorMap = customerCounselorMap;
	}

	@DisplayName("새로고침 시 데이터 전송")
	@Description("사용자 상담과 관련된 이벤트를 캐싱해두고 재접속한 경우 DAS, RAG 재요청이 아닌 캐싱 데이터 전송")
	@Test
	public void refreshSseEmitter() throws Exception {
		HttpURLConnection preConnection = (HttpURLConnection) new URL("http://localhost:" + port + "/api/v1/counseling").openConnection();
		preConnection.setRequestMethod("GET");
		preConnection.setRequestProperty("Accept", MediaType.TEXT_EVENT_STREAM_VALUE);

		String responseTaskId = "localhost-static-task-id";
		customerCounselorMap.mappingCustomerAndCounselor(CUSTOMER_PHONE_NUMBER, responseTaskId);
		emitterService.sendEvent(responseTaskId, EVENT_NAME, EVENT_DATA, true);
		emitterService.getEmitter(responseTaskId).complete();

		Thread.sleep(500);

		ResponseCookie cookie = ResponseCookie.from("task_id", responseTaskId).build();
		HttpURLConnection postConnection = (HttpURLConnection) new URL("http://localhost:" + port + "/api/v1/counseling").openConnection();
		postConnection.setRequestMethod("GET");
		postConnection.setRequestProperty("Accept", MediaType.TEXT_EVENT_STREAM_VALUE);
		postConnection.setRequestProperty("Cookie", cookie.toString());

		BufferedReader reader = new BufferedReader(new InputStreamReader(postConnection.getInputStream()));
		String event = reader.readLine().substring("event:".length());
		String data = reader.readLine().substring("data:".length());

		Assertions.assertNotNull(event);
		Assertions.assertEquals(EVENT_NAME, event);
		Assertions.assertEquals(EVENT_DATA, data);
	}
}
