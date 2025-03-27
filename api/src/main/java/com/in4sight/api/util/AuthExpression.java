package com.in4sight.api.util;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Component;

@Component
public class AuthExpression {
	private final List<String> preAllowedList;

	public AuthExpression() {
		preAllowedList = new ArrayList<>();
	}

	/**
	 * 정규식으로 접속 가능 IP를 정의
	 * @param ip Request IP
	 * @param regex 접속 허용 IP 패턴
	 * @return 인가 여부
	 */
	public boolean matchIpByRegex(String ip, String regex) {
		return ip.matches(regex);
	}

	/**
	 * 리스트에 포함되는 IP 인가
	 * @param ip Request Ip
	 * @return 인가 여부
	 */
	public boolean matchIpByAllowedList(String ip) {
		return preAllowedList.contains(ip);
	}
}
