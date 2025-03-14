package com.in4sight.api.service;

import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.in4sight.api.domain.Customer;
import com.in4sight.api.dto.CustomerRequestDto;
import com.in4sight.api.dto.CustomerResponseDto;
import com.in4sight.api.repository.CustomerRepository;

@Slf4j
@Service
@AllArgsConstructor
public class CustomerService {

	private final CustomerRepository customerRepository;

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

}
