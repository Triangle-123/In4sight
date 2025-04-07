package com.in4sight.api.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.in4sight.api.domain.ModelInfo;

@Repository
public interface ModelInfoRepository extends JpaRepository<ModelInfo, String> {
	ModelInfo findByModelSuffix(String modelSuffix);
}
