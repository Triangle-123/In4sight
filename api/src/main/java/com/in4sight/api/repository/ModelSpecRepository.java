package com.in4sight.api.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.in4sight.api.domain.ModelSpec;

@Repository
public interface ModelSpecRepository extends JpaRepository<ModelSpec, Integer> {
	List<ModelSpec> findByModelInfo_ModelSuffix(String modelSuffix);
}
