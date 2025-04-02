package com.in4sight.api.repository;

import java.util.HashMap;
import java.util.Map;

import org.springframework.stereotype.Component;

@Component
public class CustomerEventCacheRepository {
	private final Map<String, Map<String, Object>> map;

	public CustomerEventCacheRepository() {
		map = new HashMap<>();
	}

	public void addCache(String customerPhoneNumber, String eventName, Object data) {
		if (!map.containsKey(customerPhoneNumber)) {
			map.put(customerPhoneNumber, new HashMap<>());
		}
		map.get(customerPhoneNumber).put(eventName, data);
	}

	public Map<String, Object> getCache(String customerPhoneNumber) {
		return map.get(customerPhoneNumber);
	}

	public void removeCache(String customerPhoneNumber) {
		map.remove(customerPhoneNumber);
	}
}
