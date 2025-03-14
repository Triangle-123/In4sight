package com.in4sight.api.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.in4sight.api.domain.Device;
import com.in4sight.api.dto.DeviceResponseDto;
import com.in4sight.api.repository.DeviceRepository;

@Slf4j
@Service
@AllArgsConstructor
public class DeviceService {
	private final DeviceRepository deviceRepository;

	public List<DeviceResponseDto> findDevice(int customerId) {
		List<Device> devices = deviceRepository.findByCustomer_CustomerId(customerId);
		List<DeviceResponseDto> deviceResponseDtos = new ArrayList<>();
		for (Device device : devices) {
			deviceResponseDtos.add(DeviceResponseDto.builder()
				.serialNumber(device.getSerialNumber())
				.productType(device.getProductType())
				.modelSuffix(device.getModelSuffix())
				.launchDate(device.getLaunchDate())
				.build());
		}
		return deviceResponseDtos;
	}
}
