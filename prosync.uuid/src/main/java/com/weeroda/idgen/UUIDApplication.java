package com.weeroda.idgen;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


@SpringBootApplication
public class UUIDApplication {

	public static void main(String[] args) {
		System.setProperty("server.servlet.context-path", "/uuid");
		SpringApplication.run(UUIDApplication.class, args);
	}

}
