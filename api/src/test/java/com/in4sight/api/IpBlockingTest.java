package com.in4sight.api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import jdk.jfr.Description;

import com.in4sight.api.repository.AllowIpRepository;

@DisplayName("IP에 따른 인가 테스트")
@SpringBootTest
@AutoConfigureMockMvc
public class IpBlockingTest {
	private final AllowIpRepository allowIpRepository;
	private final MockMvc mockMvc;

	private static List<String> ipList;

	@Autowired
	public IpBlockingTest(AllowIpRepository allowIpRepository, MockMvc mockMvc) {
		this.allowIpRepository = allowIpRepository;
		this.mockMvc = mockMvc;
	}

	@BeforeAll
	static void setUp() {
		ipList = new ArrayList<>();
		ipList.add("192.168.0.1");
		ipList.add("192.168.0.2");
		ipList.add("172.10.0.3");
		ipList.add("172.10.0.4");
	}

	@DisplayName("사설IP만 가능")
	@Description("192.168. 으로 시작하는 IP의 정규식 표현으로 접근 허용")
	@Test
	public void allowPrivateIpTest() throws Exception {
		String regex = "^192\\.168\\..*\\..*$";

		mockExpect(
			getExpectedResultByRegex(ipList, regex),
			"/api/v1/test/allow-private-ip"
		);
	}

	@DisplayName("모든 IP 접근 거부")
	@Description("정규식을 통해 모든 접근에 대해 403")
	@Test
	public void denyAllIpTest() throws Exception {
		String regex = "^$";
		mockExpect(
			getExpectedResultByRegex(ipList, regex),
			"/api/v1/test/deny-all-ip"
		);
	}

	@DisplayName("임의 지정한 IP 접근 가능")
	@Description("Allow List를 통해 접근 가능 IP를 제어")
	@Test
	public void allowIpListTest() throws Exception {
		allowIpRepository.add(ipList.get(1));
		allowIpRepository.add(ipList.get(2));

		mockExpect(
			getExpectedResultByList(ipList),
			"/api/v1/test/allow-list-ip"
		);
	}

	private boolean[] getExpectedResultByList(List<String> ipList) {
		boolean[] expectedResult = new boolean[ipList.size()];

		for (int i = 0; i < ipList.size(); i++) {
			expectedResult[i] = allowIpRepository.contains(ipList.get(i));
		}

		return expectedResult;
	}

	private boolean[] getExpectedResultByRegex(List<String> ipList, String regex) {
		boolean[] expectedResult = new boolean[ipList.size()];

		for (int i = 0; i < ipList.size(); i++) {
			expectedResult[i] = ipList.get(i).matches(regex);
		}

		return expectedResult;
	}

	private void mockExpect(boolean[] expectedResult, String urlTemplate) throws Exception {
		for (int i = 0; i < ipList.size(); i++) {
			mockMvc
				.perform(get(urlTemplate)
					.header("X-Forwarded-For", ipList.get(i)))
				.andExpect(expectedResult[i] ? status().isOk() : status().isForbidden());
		}
	}
}
