package com.in4sight.api.exception;

public class NotFoundCounselorException extends RuntimeException {
	public NotFoundCounselorException(String phoneNumber) {
		super("가용 가능한 상담 세션 없음, 고객 전화번호 : " + phoneNumber);
	}
}
