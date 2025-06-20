package com.in4sight.api.service;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.in4sight.api.domain.Customer;
import com.in4sight.api.dto.CustomerResponseDto;
import com.in4sight.api.exception.NotFoundCounselorException;
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

	public CustomerResponseDto findCustomer(String phoneNumber) {
		Customer customer = customerRepository.findByPhoneNumber(phoneNumber);
		return CustomerResponseDto.builder()
			.customerId(customer.getCustomerId())
			.customerName(customer.getCustomerName())
			.phoneNumber(customer.getPhoneNumber())
			.address(customer.getAddress())
			.build();
	}

	/**
	 * 고객과 상담사의 연결 시작
	 *
	 * @param phoneNumber 연결할 고객의 전화번호
	 */
	public void connectingCustomerAndCounselor(String phoneNumber) {

		long startTime = System.currentTimeMillis();
		ScheduledExecutorService executor = Executors.newScheduledThreadPool(1);

		Runnable scheduledTask = new Runnable() {
			@Override
			public void run() {
				try {
					if (System.currentTimeMillis() - startTime > 5000) {
						throw new NotFoundCounselorException(phoneNumber);
					} else {
						if (customerCounselorMap.getMappedCounselor(phoneNumber) != null) {
							log.info(customerCounselorMap.getMappedCounselor(phoneNumber));
							CustomerResponseDto unconnectedCustomer = findCustomer(phoneNumber);
							executor.shutdown();
							throw new Exception("이미 상담중인 고객, 전화번호 : " + phoneNumber);
						}
						String availableCounselor;
						do {
							availableCounselor = customerCounselorMap.getAvailableCounselorTaskId();
						} while (customerCounselorMap.getMappedCustomer(availableCounselor) != null
							|| emitterService.getEmitter(availableCounselor) == null);
						customerCounselorMap.mappingCustomerAndCounselor(phoneNumber, availableCounselor);
						CustomerResponseDto connectedCustomer = findCustomer(phoneNumber);
						emitterService.startProcess(availableCounselor, connectedCustomer);
						executor.shutdown();
					}
				} catch (NullPointerException e) {
					log.error(e.getMessage());
					log.info("retry mapping counselor...");
				} catch (NotFoundCounselorException e) {
					log.error(e.getMessage());
					executor.shutdown();
				} catch (Exception e) {
					log.error(e.getMessage());
				}
			}
		};
		executor.scheduleWithFixedDelay(scheduledTask, 0, 500, TimeUnit.MILLISECONDS);
	}

	/**
	 * 고객과 상담사의 연결 종료
	 *
	 * @param phoneNumber 연결을 종료할 고객의 전화번호
	 */
	public void disconnectCustomerAndCounselor(String phoneNumber) {
		String taskId = customerCounselorMap.removeCustomer(phoneNumber);
		CustomerResponseDto disconnectCustomer = findCustomer(phoneNumber);

		emitterService.sendEvent(taskId, "customer_disconnect", disconnectCustomer);
		// Logging 이후 Redis를 통해 Counseling Log DB에 데이터 저장하는 로직을 추가
		eventCacheRepository.removeCache(disconnectCustomer.getPhoneNumber());
	}

	public boolean setCustomerCallRequest(String phoneNumber) {
		if (customerCounselorMap.getMappedCounselor(phoneNumber) != null) {
			return false;
		}

		for (String taskId : customerCounselorMap.getAvailableCounselors(emitterService.getAllCounselors())) {
			emitterService.sendEvent(taskId, "request_call", findCustomer(phoneNumber));
		}

		return true;
	}

	public void solveRequest(String phoneNumber) {
		for (String taskId : customerCounselorMap.getAvailableCounselors(emitterService.getAllCounselors())) {
			emitterService.sendEvent(taskId, "request_solved", findCustomer(phoneNumber));
		}
	}
}
