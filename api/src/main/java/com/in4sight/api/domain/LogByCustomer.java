package com.in4sight.api.domain;

import java.util.List;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import lombok.ToString;

@Document("log_by_customer")
@Getter
@RequiredArgsConstructor
@NoArgsConstructor(force = true)
@ToString
public class LogByCustomer {

	@Id
	private String id;

	@Field("customer_id")
	private final int customerId;

	@Field("counseling_history")
	private final List<CounselingHistory> counselingHistory;
}
