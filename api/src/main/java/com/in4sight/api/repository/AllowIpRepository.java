package com.in4sight.api.repository;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Component;

@Component
public class AllowIpRepository {
	private final List<String> list;

	public AllowIpRepository() {
		this.list = new ArrayList<>();
	}

	public void add(String ip) {
		list.add(ip);
	}

	public boolean contains(String ip) {
		return list.contains(ip);
	}
}
