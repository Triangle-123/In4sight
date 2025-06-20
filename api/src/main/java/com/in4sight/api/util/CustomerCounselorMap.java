package com.in4sight.api.util;

import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.stream.Collectors;

import org.springframework.stereotype.Component;

/**
 * 상담원과 고객을 연결을 관리하는 자료구조
 */
@Component
public class CustomerCounselorMap {

	private final ConcurrentHashMap<String, String> mappedCustomer;
	private final Map<String, String> mappedCounselor;
	private final Queue<String> availableCounselors;

	public CustomerCounselorMap() {
		this.mappedCustomer = new ConcurrentHashMap<>();
		this.mappedCounselor = new ConcurrentHashMap<>();
		this.availableCounselors = new ConcurrentLinkedQueue<>();
	}

	/**
	 * 사용가능한 상담원 SSE TaskID 확인
	 * @return 상담원 SSE TaskID 반환
	 */
	public synchronized String getAvailableCounselorTaskId() {
		return availableCounselors.poll();
	}

	/**
	 * 상담원 TaskID Queue 삽입
	 * @param counselor 상담원 TaskID
	 */
	public void setAvailableCounselor(String counselor) {
		availableCounselors.offer(counselor);
	}

	/**
	 * 고객과 상담원을 연결
	 * @param customer 고객 전화 번호
	 * @param counselor 상담원 TaskID
	 * @throws Exception 이미 다른 사용자가 해당 상담원을 점유하고 있는 경우
	 */
	public void mappingCustomerAndCounselor(String customer, String counselor) throws Exception {
		String customerExists = mappedCustomer.putIfAbsent(counselor, customer);

		if (customerExists != null) {
			throw new Exception(String.format("Customer %s already exists", customer));
		}

		mappedCounselor.put(customer, counselor);
	}

	/**
	 * 고객과 상담원의 연결을 해지
	 * @param customer 고객 전화 번호
	 * @return 다시 Queue 에 들어가서 상담 가능한 상담원의 TaskId
	 */
	public String removeCustomer(String customer) {
		String reAvailableCounselor = mappedCounselor.remove(customer);
		mappedCustomer.remove(reAvailableCounselor);
		setAvailableCounselor(reAvailableCounselor);

		return reAvailableCounselor;
	}

	/**
	 * 상담원 Task Id에 매칭된 고객이 있는 경우 반환
	 * @param counselor 상담원의 Task Id
	 * @return 고객의 전화번호
	 */
	public String getMappedCustomer(String counselor) {
		return mappedCustomer.getOrDefault(counselor, null);
	}


	/**
	 * 해당 고객에 이미 매칭된 상담사가 있는 경우 반환
	 * @param phoneNumber
	 * @return 상담사 Task Id
	 */
	public String getMappedCounselor(String phoneNumber) {
		return mappedCounselor.getOrDefault(phoneNumber, null);
	}

	public Set<String> getAvailableCounselors(Set<String> counselors) {
		return counselors.stream()
			.filter(counselor -> !mappedCounselor.containsKey(counselor))
			.collect(Collectors.toSet());
	}

}
