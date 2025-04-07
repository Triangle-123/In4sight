package com.in4sight.api.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.in4sight.api.domain.ModelFeature;

@Repository
public interface ModelFeatureRepository extends JpaRepository<ModelFeature, Integer> {
	List<ModelFeature> findByModelInfo_ModelSuffix(String modelSuffix);
}
