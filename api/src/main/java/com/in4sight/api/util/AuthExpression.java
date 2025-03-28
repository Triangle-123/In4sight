package com.in4sight.api.util;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.in4sight.api.repository.AllowIpRepository;

@Component
public class AuthExpression {
	private final AllowIpRepository allowIpRepository;

	@Autowired
	public AuthExpression(AllowIpRepository allowIpRepository) {
		this.allowIpRepository = allowIpRepository;
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
		return allowIpRepository.contains(ip);
	}
}
