package com.in4sight.api.domain;

import java.time.LocalDate;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Entity
@Getter
@NoArgsConstructor
@AllArgsConstructor
@ToString
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Device {

	@Id
	@EqualsAndHashCode.Include
	@Column(name = "serial_number")
	private String serialNumber;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "customer_id", nullable = false)
	private Customer customer;

	@Column(name = "product_type", nullable = false)
	private String productType;

	@Column(name = "model_suffix", nullable = false)
	private String modelSuffix;

	@Column(name = "model_name", nullable = false)
	private String modelName;

	@Column(name = "launch_date", nullable = false)
	private LocalDate launchDate;
}
