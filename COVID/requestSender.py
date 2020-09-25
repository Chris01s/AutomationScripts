import requests
import sys
from urllib.parse import urlparse


class Request:
	def __init__(self, url):
		self.url = url
		self.headers = {
         "Content-Type": 'text/css; charset=utf-8',
         "Accept": 'text/css,json,*/*;q=0.1',
         "User-Agent":'''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/78.0.3904.97 Chrome/78.0.3904.97 Safari/537.36'''
     }
	
	def send_request(self):
		try:
			self.response = requests.get(
				url = self.url,
				headers = self.headers
			)
			if self.response.status_code == 200:
				print(f"[+] Response received from {self.url}: {self.response.reason}")
		except Exception as ex:
			print(f"[!] Unexpected error...{ex.__str__()}")
			print(f"[!] {self.response.reason}")
			sys.exit()
	
	def parse_link(self, base_url, link):
		link_parsed = urlparse(link)
		base_url_parsed = urlparse(base_url)
		if not link_parsed.scheme and not link_parsed.netloc:
			return base_url_parsed.scheme+"://"+base_url_parsed.netloc+link
		else:
			return link
	

