#!/bin/python

import requests


class GetRequests:
	def __init__(self, url, add_proxies = False):
		self.url = url
		self.add_proxies = add_proxies
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0)'
							  ' Gecko/20100101 Firefox/60.0',
			'Accept': 'application/json, text/javascript, */*; q=0.01'
		}
		self.proxies = {
			'http': 'socks5://127.0.0.1:9050'
		}
	def send_get_request(self):
		if self.add_proxies:
		 	self.response = requests.get(
		 		url = self.url,
		 		headers = self.headers,
		 		proxies = self.proxies
		 	)
		else:
			self.response = requests.get(
		 		url = self.url,
		 		headers = self.headers
		 	)
	
	def get_status_code(self):
		self.status_code = self.response.status_code
