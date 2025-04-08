package com.in4sight.api.domain;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Entity
@Table(name = "model_info")
@Getter
@NoArgsConstructor
@AllArgsConstructor
@ToString
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class ModelInfo {

	@Id
	@EqualsAndHashCode.Include
	@Column(name = "model_suffix", nullable = false)
	private String modelSuffix;

	@Column(name = "model_name", nullable = false)
	private String modelName;

	@Column(name = "product_type", nullable = false)
	private String productType;

	@Column(name = "purchase_date", nullable = false)
	private String purchaseDate;

	@Column(name = "model_image", nullable = false)
	private String modelImage;

	@OneToMany(mappedBy = "modelInfo", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
	private List<Device> devices;

	@OneToMany(mappedBy = "modelInfo", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
	private List<ModelSpec> modelSpecs;

	@OneToMany(mappedBy = "modelInfo", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
	private List<ModelFeature> modelFeatures;
}
