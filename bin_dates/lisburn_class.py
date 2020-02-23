#!/bin/python

import sys
import time
from bs4 import BeautifulSoup
import requests


class LisburnBinCollections:
	def __init__(self, address, postcode):
		self.url = 'https://lisburncastlereagh.gov.uk/resident/bins-recycling/when-is-my-bin-collection-day'
		self.address = address
		self.postcode = postcode
		self.headers = {
			"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
							'AppleWebKit/537.36 (KHTML, like Gecko) '
							'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
			"Connection": "keep-alive",
			"Accept": "application/json"
		}
		self.post_data = [
        ("method", "POST"),
        ('searchtext', self.address.upper()+" LISBURN "+self.postcode.upper()),
        ("id","addressResults")
    	]
    
		
	def send_get_request(self):
		 self.response = requests.get(
		 	url = self.url,
		 	headers = self.headers
		 )
		 
	
	def get_markup(self):
		self.markup = self.response.text 
		
		
	def get_soup(self):
		 self.soup = BeautifulSoup(
		 	markup = self.markup,
		 	features = "lxml"
		 )
		 
	
	def get_iframe_src_url(self):
		self.url = self.soup.find_all("iframe")[0]["src"]


	def send_post_request_to_iframe(self):
		 self.response = requests.post(
		     url = self.url,
		     data = self.post_data
		 )
		 
		 
	def get_results_url(self):
		self.result_url = self.soup.find("a")['href']


	def get_next_collections(self):
		 self.next_collections = self.soup.find("div", {"id":"nextCollectionSection"})
		 
		 
	def get_bin_collection_dates(self):
		 self.bin_dates = self.next_collections.find_all("h5")


	def get_bin_collection_types(self):
		 self.bin_types = self.next_collections.find_all("ul")
		
	
	def scrape_bin_dates(self):
		print("Sending GET request to bin site...")    
		self.send_get_request()
		print("Request status:", self.response.status_code, "\n")
		
		self.get_markup()
		self.get_soup()
		self.get_iframe_src_url()		
		
		print("Sending POST request to bin site...")    
		self.send_post_request_to_iframe()
		print("Request status:", self.response.status_code, "\n")

		self.get_markup()
		self.get_soup()
		self.get_results_url()
		self.url += self.result_url[1:]
		print("Sending GET request to results page...")    
		self.send_get_request()
		print("Request status:", self.response.status_code, "\n")
		
		self.get_markup()
		self.get_soup()
		self.get_next_collections()
		self.get_bin_collection_dates()
		self.get_bin_collection_types()
		
		print("results...")    
		for bin_type, bin_date in zip(self.bin_types, self.bin_dates):
			print(bin_date.text+":",bin_type.text)


