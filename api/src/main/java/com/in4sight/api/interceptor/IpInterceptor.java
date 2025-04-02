package com.in4sight.api.interceptor;

import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Component
public class IpInterceptor implements HandlerInterceptor {

	public static final String IPV6_ATTRIBUTE_KEY = "CLIENT_IDV6";
	public static final String IPV4_ATTRIBUTE_KEY = "CLIENT_IPV4";

	@Override
	public boolean preHandle(
		HttpServletRequest request,
		HttpServletResponse response,
		Object handler
	) throws Exception {

		String ip = extractIP(request);
		log.info(ip);
		request.setAttribute(IPV4_ATTRIBUTE_KEY, convertIpV4(ip));
		request.setAttribute(IPV6_ATTRIBUTE_KEY, convertIpV6(ip));
		return HandlerInterceptor.super.preHandle(request, response, handler);
	}

	private String extractIP(HttpServletRequest request) {

		String[] headers = {
			"X-Forwarded-For",
			"Proxy-Client-IP",
			"WL-Proxy-Client-IP",
			"HTTP_CLIENT_IP",
			"HTTP_X_FORWARDED_FOR",
			"HTTP_X_FORWARDED",
			"HTTP_X_CLUSTER_CLIENT_IP",
			"HTTP_CLIENT_CLUSTER_IP",
			"HTTP_FORWARDED_FOR",
			"HTTP_FORWARDED"
		};

		for (String header : headers) {
			String ip = request.getHeader(header);
			if (ip != null && !ip.isEmpty() && !"unknown".equalsIgnoreCase(ip)) {
				if (ip.contains(",")) {
					ip = ip.split(",")[0];
				}
				return ip;
			}
		}

		return request.getRemoteAddr();
	}

	private String convertIpV4(String ip) {
		if (ip.contains(":")) {
			if (ip.equals("0:0:0:0:0:0:0:1")) {
				ip = "127.0.0.1";
			} else if (ip.startsWith("::ffff:")) {
				ip = ip.substring("::ffff:".length());
			} else if (ip.startsWith("0:0:0:0:0:ffff:")) {
				ip = ip.substring("0:0:0:0:0:0:ffff:".length());
			}
		}

		return ip;
	}

	private String convertIpV6(String ip) {
		if (!ip.contains(":")) {
			ip = "::ffff:" + ip;
		}

		return ip;
	}
}
