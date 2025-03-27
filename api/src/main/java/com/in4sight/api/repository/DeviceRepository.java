package com.in4sight.api.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.in4sight.api.domain.Device;

@Repository
public interface DeviceRepository extends JpaRepository<Device, String> {
	List<Device> findByCustomer_CustomerId(int customerId);
}
