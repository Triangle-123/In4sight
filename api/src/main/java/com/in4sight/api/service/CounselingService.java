package com.in4sight.api.service;

import java.util.List;

import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.in4sight.api.domain.CustomerDevice;
import com.in4sight.api.domain.LogByCustomer;
import com.in4sight.api.repository.CounselingRepository;

@Slf4j
@Service
@AllArgsConstructor
public class CounselingService {

	private final CounselingRepository counselingRepository;
	private final MongoTemplate mongoTemplate;

	public void addLog(int customerId, String counselingDate, List<CustomerDevice> devices) {
//		counselingRepository.deleteAll();
//		Query query = new Query(
//			Criteria.where("customer_id").is(customerId)
//		);
//
//		Update update = new Update().push("counseling_history", new CounselingHistory(counselingDate, devices));
//		mongoTemplate.upsert(query, update, LogByCustomer.class);
	}

	public LogByCustomer findLog(int customerId) {
		return counselingRepository.findByCustomerId(customerId);
	}

	public void replaceLogByDevice(int customerId, String counselingDate, CustomerDevice device) {
//		Query query = new Query(
//			Criteria.where("customer_id").is(customerId)
//				.and("counseling_history.counseling_date").is(counselingDate)
//				.and("counseling_history.devices.serial_number").is(device.getSerialNumber())
//		);
//
//		Update update = new Update()
//			.set("counseling_history.$[outer].devices.$[inner]", device);
//
//		update.filterArray("outer.counseling_date", counselingDate)
//			.filterArray("inner.serial_number", device.getSerialNumber());
//
//		log.info("replace");
//		log.info("Generated Query: " + query);
//		log.info("device : {}", device);
//		UpdateResult result = mongoTemplate.updateFirst(query, update, LogByCustomer.class);
//		log.info("Matched count: " + result.getMatchedCount());
//		log.info("Modified count: " + result.getModifiedCount());
	}

}
