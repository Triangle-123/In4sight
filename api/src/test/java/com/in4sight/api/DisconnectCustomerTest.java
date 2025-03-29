package com.in4sight.api;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.context.bean.override.mockito.MockitoSpyBean;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;

import jdk.jfr.Description;

import com.in4sight.api.controller.TriggerController;
import com.in4sight.api.domain.Customer;
import com.in4sight.api.dto.CustomerResponseDto;
import com.in4sight.api.repository.CustomerRepository;
import com.in4sight.api.service.CustomerService;
import com.in4sight.api.service.EmitterService;
import com.in4sight.api.util.CustomerCounselorMap;


@DisplayName("사용자 연결 종료 테스트")
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class DisconnectCustomerTest {

	@LocalServerPort
	private int port;

	private final CustomerCounselorMap customerCounselorMap;
	private final TriggerController triggerController;

	@MockitoBean
	private CustomerRepository customerRepository;

	@MockitoSpyBean
	private EmitterService emitterService;

	@MockitoSpyBean
	private CustomerService customerService;

	private static String customerPhoneNumber;
	private static CustomerResponseDto customerResponseDto;
	private static SseEmitter emitter;
	private static final String TASK_ID = "test";

	@Autowired
	public DisconnectCustomerTest(
		CustomerCounselorMap customerCounselorMap,
		TriggerController triggerController
	) {
		this.customerCounselorMap = customerCounselorMap;
		this.triggerController = triggerController;
	}

	@BeforeAll
	static void setUp() {
		customerPhoneNumber = "010-1234-5678";

		customerResponseDto = new CustomerResponseDto(
			1,
			"최싸피",
			"010-1234-5678",
			"테스트 주소"
		);
		emitter = new SseEmitter(1000 * 60L);
	}

	@DisplayName("사용자가 통화 종료이후 연결 제거")
	@Description("연결제거 이후 SSE를 통해 데이터가 전달되었는지 확인하고, 가용가능한 상담사에 리소스를 반환했는지 확인")
	@Test
	public void testSendEvent() throws Exception {
		Mockito.when(
			customerRepository.findByPhoneNumber(customerPhoneNumber)
		).thenReturn(new Customer());
		Mockito.when(customerService.findCustomer(customerPhoneNumber)).thenReturn(customerResponseDto);
		Mockito.when(emitterService.getEmitter(TASK_ID)).thenReturn(emitter);

		customerCounselorMap.mappingCustomerAndCounselor(customerPhoneNumber, TASK_ID);

		HttpURLConnection connection = (HttpURLConnection) new URL("http://localhost:" + port + "/api/test/counseling?task_id=" + TASK_ID).openConnection();
		connection.setRequestMethod("GET");
		connection.setRequestProperty("Accept", MediaType.TEXT_EVENT_STREAM_VALUE);

		triggerController.endPhoneCall(customerPhoneNumber);

		Assertions.assertEquals(200, connection.getResponseCode());
		Assertions.assertEquals(MediaType.TEXT_EVENT_STREAM_VALUE, connection.getContentType());

		BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
		String event = reader.readLine().substring("event:".length());
		ObjectMapper mapper = new ObjectMapper();
		mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
		String stringData = reader.readLine().substring("data:".length());
		CustomerResponseDto data = mapper.readValue(stringData, CustomerResponseDto.class);

		Assertions.assertNotNull(event);
		Assertions.assertEquals("customer_disconnect", event);
		Assertions.assertEquals(customerResponseDto.toString(), data.toString());

		Assertions.assertEquals(TASK_ID, customerCounselorMap.getAvailableCounselorTaskId());
	}
}
