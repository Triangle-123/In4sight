package com.in4sight.api.service;

import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.in4sight.api.domain.Customer;
import com.in4sight.api.dto.CustomerRequestDto;
import com.in4sight.api.dto.CustomerResponseDto;
import com.in4sight.api.repository.CustomerEventCacheRepository;
import com.in4sight.api.repository.CustomerRepository;
import com.in4sight.api.util.CustomerCounselorMap;

@Slf4j
@Service
@AllArgsConstructor
public class CustomerService {

	private final CustomerRepository customerRepository;
	private final EmitterService emitterService;
	private final CustomerCounselorMap customerCounselorMap;
	private final CustomerEventCacheRepository eventCacheRepository;

	public CustomerResponseDto findCustomer(CustomerRequestDto customerRequestDto) {
		Customer customer = customerRepository.findByCustomerNameAndPhoneNumber(
				customerRequestDto.getCustomerName(),
				customerRequestDto.getPhoneNumber()
		);
		return CustomerResponseDto.builder()
				.customerId(customer.getCustomerId())
				.customerName(customer.getCustomerName())
				.phoneNumber(customer.getPhoneNumber())
				.address(customer.getAddress())
				.build();
	}

	/**
	 * 고객과 상담사의 연결 종료
	 * @param customerRequestDto 연결을 종료할 고객의 정보
	 */
	public void disconnectCustomerAndCounselor(CustomerRequestDto customerRequestDto) {
		String taskId = customerCounselorMap.removeCustomer(customerRequestDto.getPhoneNumber());
		CustomerResponseDto disconnectCustomer = findCustomer(customerRequestDto);

		emitterService.sendEvent(taskId, "customer_disconnect", disconnectCustomer);
		// Logging 이후 Redis를 통해 Counseling Log DB에 데이터 저장하는 로직을 추가
		eventCacheRepository.removeCache(disconnectCustomer.getPhoneNumber());
	}

}
