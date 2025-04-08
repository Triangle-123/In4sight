package com.in4sight.api.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.in4sight.api.domain.Device;
import com.in4sight.api.domain.ModelFeature;
import com.in4sight.api.domain.ModelInfo;
import com.in4sight.api.domain.ModelSpec;
import com.in4sight.api.dto.DeviceResponseDto;
import com.in4sight.api.dto.ModelFeatureResponseDto;
import com.in4sight.api.dto.ModelInfoResponseDto;
import com.in4sight.api.dto.ModelSpecResponseDto;
import com.in4sight.api.repository.DeviceRepository;
import com.in4sight.api.repository.ModelFeatureRepository;
import com.in4sight.api.repository.ModelInfoRepository;
import com.in4sight.api.repository.ModelSpecRepository;

@Slf4j
@Service
@AllArgsConstructor
public class DeviceService {
	private final DeviceRepository deviceRepository;
	private final ModelInfoRepository modelInfoRepository;
	private final ModelSpecRepository modelSpecRepository;
	private final ModelFeatureRepository modelFeatureRepository;

	public List<DeviceResponseDto> findDevice(int customerId) {
		List<Device> devices = deviceRepository.findByCustomer_CustomerId(customerId);
		List<DeviceResponseDto> deviceResponseDtos = new ArrayList<>();

		for (Device device : devices) {
			String modelSuffix = device.getModelInfo().getModelSuffix();
			ModelInfo modelInfo = modelInfoRepository.findByModelSuffix(modelSuffix);
			List<ModelSpec> modelSpecs = modelSpecRepository.findByModelInfo_ModelSuffix(modelSuffix);
			List<ModelSpecResponseDto> modelSpecResponseDtos = new ArrayList<>();
			List<ModelFeature> modelFeatures = modelFeatureRepository.findByModelInfo_ModelSuffix(modelSuffix);
			List<ModelFeatureResponseDto> modelFeatureResponseDtos = new ArrayList<>();
			for (ModelSpec spec : modelSpecs) {
				modelSpecResponseDtos.add(ModelSpecResponseDto.builder()
					.specGroup(spec.getSpecGroup())
					.specName(spec.getSpecName())
					.specValue(spec.getSpecValue())
					.build());
			}
			for (ModelFeature feature : modelFeatures) {
				modelFeatureResponseDtos.add(ModelFeatureResponseDto.builder()
					.featureName(feature.getFeatureName())
					.build());
			}
			deviceResponseDtos.add(DeviceResponseDto.builder()
				.serialNumber(device.getSerialNumber())
				.modelInfo(ModelInfoResponseDto.builder()
					.modelSuffix(modelInfo.getModelSuffix())
					.modelName(modelInfo.getModelName())
					.productType(modelInfo.getProductType())
					.launchDate(modelInfo.getLaunchDate())
					.modelImage(modelInfo.getModelImage())
					.build())
				.modelSpecs(modelSpecResponseDtos)
				.modelFeatures(modelFeatureResponseDtos)
				.build());
		}
		return deviceResponseDtos;
	}
}
