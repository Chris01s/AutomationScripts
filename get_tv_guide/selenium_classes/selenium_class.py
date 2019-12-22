#!/bin/python

from selenium import webdriver
import sys
import json
import re


class GetSelenium:
	def __init__(self, url, add_proxies = False):
		self.url = url
		self.add_proxies = add_proxies
		
	def get_firefox_driver(self):	
		self.firefox_options = webdriver.FirefoxOptions()
		self.firefox_options.add_argument("--headless")
		if self.add_proxies:
			self.firefox_options.add_argument(
				"--proxy-server=socks5://127.0.0.1:9050"
			)
		self.driver = webdriver.Firefox(
			executable_path = "/usr/bin/geckodriver",
			options = self.firefox_options
		)
	
	def get_chrome_driver(self):
		self.chrome_options = webdriver.ChromeOptions()
		self.chrome_options.add_argument("--headless")
		if self.add_proxies:
			self.chrome_options.add_argument(
				"--proxy-server=socks5://127.0.0.1:9050"
			)
		self.driver = webdriver.Chrome(
			executable_path="/usr/bin/chromedriver",
			options = self.chrome_options
		)
		
	def start_driver(self):
		self.driver.get(self.url)
	
	def retrieve_status_code(self):
		if self.driver.page_source:
			self.status_code = 200
		else:
			self.status_code = 401
			
	def close_driver(self):
		try:
			self.driver.close()
			self.driver.quit()
		except:
			try:
				os.system("killall geckodriver")
				os.system("killall firefox")
			except:
				pass
		
