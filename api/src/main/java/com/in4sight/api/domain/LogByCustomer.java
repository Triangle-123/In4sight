package com.in4sight.api.domain;

import java.util.List;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Document("log_by_customer")
@Data
@NoArgsConstructor
@ToString
public class LogByCustomer {

	@Id
	private String id;

	@Field("customer_id")
	private int customerId;

	@Field("counseling_history")
	private List<CounselingHistory> counselingHistory;

}
