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

@DisplayName("상담사 연결 테스트")
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class CounselorConnectTest {
	@LocalServerPort
	private int port;

	private final EmitterService emitterService;
	private final CustomerCounselorMap customerCounselorMap;

	@Autowired
	public CounselorConnectTest(
		EmitterService emitterService,
		CustomerCounselorMap customerCounselorMap
	) {
		this.emitterService = emitterService;
		this.customerCounselorMap = customerCounselorMap;
	}

	@DisplayName("상담사 최초 접속")
	@Description("상담사 프론트 페이지 최초 접속시 Cookie를 통해서 Task ID 발급")
	@Test
	public void counselorIssueTaskIdTest() throws Exception {
		HttpURLConnection connection = (HttpURLConnection) new URL("http://localhost:" + port + "/api/v1/counseling").openConnection();
		connection.setRequestMethod("GET");
		connection.setRequestProperty("Accept", MediaType.TEXT_EVENT_STREAM_VALUE);

		Assertions.assertEquals(HttpURLConnection.HTTP_OK, connection.getResponseCode());
		Assertions.assertEquals(MediaType.TEXT_EVENT_STREAM_VALUE, connection.getContentType());

		BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
		String line = reader.readLine();
		Assertions.assertNotNull(line);
		Assertions.assertNotNull(connection.getHeaderField("Set-Cookie"));
	}

	@DisplayName("상담사 재접속")
	@Description("상담사 프론트 페이지 재접속시 Cookie의 값을 Task ID 특정")
	@Test
	public void counselorUsedCookieTest() throws Exception {
		String cookieValue = "counselor";
		ResponseCookie cookie = ResponseCookie.from("task_id", cookieValue).build();

		HttpURLConnection connection = (HttpURLConnection) new URL("http://localhost:" + port + "/api/v1/counseling").openConnection();
		connection.setRequestMethod("GET");
		connection.setRequestProperty("Accept", MediaType.TEXT_EVENT_STREAM_VALUE);
		connection.setRequestProperty("Cookie", cookie.toString());

		String responseTaskId = connection.getHeaderField("Set-Cookie").split(";")[0].substring("task_id=".length());
		Assertions.assertEquals(cookieValue, responseTaskId);

		Assertions.assertNotNull(emitterService.getEmitter(responseTaskId));
		Assertions.assertEquals(responseTaskId, customerCounselorMap.getAvailableCounselorTaskId());
	}
}
