package com.in4sight.api.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.in4sight.api.domain.LogByCustomer;

@Repository
public interface CounselingRepository extends MongoRepository<LogByCustomer, String> {
	LogByCustomer findByCustomerId(String customerId);
}
