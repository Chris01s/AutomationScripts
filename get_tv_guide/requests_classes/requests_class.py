#!/bin/python

import requests


class GetRequests:
	def __init__(self, url, proxy = '', add_proxies = False):
		self.url = url
		self.add_proxies = add_proxies
		self.proxy = proxy
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0)'
							  ' Gecko/20100101 Firefox/60.0',
			'Accept': 'application/json, text/javascript, */*; q=0.01'
		}
		
	def send_get_request(self):
		if self.add_proxies:
			self.proxies = {
				'http':self.proxy,
				'https':self.proxy
			}
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
