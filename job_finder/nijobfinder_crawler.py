#!/bin/python

import sys
import requests
import codecs
from urllib.parse import urlparse
from bs4 import BeautifulSoup 


class NIJobFinderCrawl:
	def __init__(self, location, keywords, categories, Apply=False):
		self.location = location
		self.keywords = keywords.split(",")
		self.categories = categories
		self.Apply = Apply
		self.href_results = list()
		self.page_number = 1
		self.no_result = False	
	
	def encode_query(self, query): 
		query_encoded = '' 
		for char in query: 
			if char in [" ", "|", "&"]: 
				char = char.encode("ascii") 
				char = "%"+codecs.encode(char, "hex").decode("utf-8")
				char = char.upper() 
			query_encoded += char 
		return query_encoded 


	def get_url(self):
		self.categories = self.encode_query(self.categories)
		self.url = ''.join([
			"https://www.nijobfinder.co.uk/search/?",
			"locations="+self.location,
			"&sectors="+self.categories,
			"&recruiterType=Company",
			"&page="+str(self.page_number),
			"&order=Date+Added"
		])
		
		
	def get_results_page(self):
		self.headers = {
			'Accept': '*/*', 
			'Connection': 'keep-alive',
			"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
						 ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
		}
		try:
			self.result_html = requests.get(
				url = self.url,
				headers = self.headers
			)
		except Exception as ex:
			print("Something went wrong",ex.__str__())
	
	
	def get_soup(self):
		if self.result_html.status_code == 200:
			self.soup = BeautifulSoup(
				markup = self.result_html.text,
				features = "lxml"
			)
			if "We couldn't find any jobs" in self.soup.text:
				self.no_result = True
		else:
			print("Something went wrong", self.result_html.status_code)


	def get_job_results(self):
		try:
			self.job_results = self.soup.find_all(class_="c-result")
		except Exception as ex:
			print("Something went wrong",ex.__str__())
			
	
	def get_job_title(self):
		return self.element.h2.text.strip()
		
	
	def get_job_company(self):
		try:
			return self.element.p.text.strip()
		except:
			return "couldnt find"
	
	
	def get_href_link(self):
		return self.element.h2.a['href']
	
	
	def check_if_external_link(self):
		base_url_parsed = urlparse(self.url)
		href_link_parsed = urlparse(self.href_link)
		if href_link_parsed.scheme:
			pass
		else:
			self.href_link = ''.join([
				base_url_parsed.scheme,
				"://",
				base_url_parsed.netloc,
				href_link_parsed.path
			])
		
		
	def crawl_site(self):
		while not self.no_result:
			self.get_url()
			print("Scraping", self.url)
			
			self.get_results_page()
			self.get_soup()
			
			if self.no_result:
				print("No more results...")
				break
			
			self.get_job_results()
			
			for element in self.job_results:
				self.element = element
				self.job_title = self.get_job_title()
				self.job_company = self.get_job_company()
				self.href_link = self.get_href_link()
				self.check_if_external_link()
				if self.href_link in self.href_results:
					continue
				else:
					for word in self.keywords:
						if word.strip() in self.job_title.strip():
							print("\n")
							print("Job title:", self.job_title.strip()) 
							print("Company:", self.job_company.strip()) 
							print("Hyperlink:", self.href_link.strip()) 
							self.href_results.append(self.href_link.strip())
							break
			self.page_number += 1

