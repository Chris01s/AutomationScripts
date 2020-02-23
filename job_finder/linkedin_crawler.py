#!/bin/python

import sys
import codecs
import requests
import string
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class LinkedInJobCrawl:
	def __init__(self, location, keywords, Apply=False):
		self.location = location
		self.keywords = keywords.split(",")
		self.Apply = Apply
		self.href_results = list()
		self.page_number = 1
		self.no_result = False


	def get_url(self):
		self.url = ''.join([
			"https://www.linkedin.com/jobs/search?",
			"keywords="+self.keyword,
			"&location="+self.location,
			"&trk=guest_job_search_jobs",
			"-search-bar_search-submit&",
			"redirect=false&position=1&pageNum=0",
			"f_TP=1%2C2%2C3%2C4"
		])


	def hexify_keyword(self):
		for punct in string.punctuation+" ":
			binarized_text = bytes(punct, "ascii")
			hexified_text = codecs.encode(binarized_text, "hex")
			self.keyword = self.keyword.replace(
				punct, "%"+hexified_text.decode("ascii")
			)


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
			if "No jobs were found to match your criteria" in self.soup.text:
				self.no_result = True
		else:
			print("Something went wrong", self.result_html.status_code)


	def get_job_results(self):
		try:
			self.job_results = self.soup.find_all("li",{"class":"result-card"})
		except Exception as ex:
			print("Something went wrong",ex.__str__())



	def get_job_title(self):
		self.job_title = self.element.h3.text


	def get_job_company(self):
		try:
			self.job_company = self.element.h4.text
		except Exception as ex:
			print("Something went wrong",ex.__str__())


	def get_job_weblink(self):
		try:
			self.href_link = self.element.a['href']
		except Exception as ex:
			print("Something went wrong",ex.__str__())


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


	def check_if_more_results(self):
		self.more_results = self.soup.find("button", {"class":"see-more-jobs"})
		if self.more_results:
			self.no_more_results = False
		else:
			self.no_more_results = True


	def scrape_results(self):
		for element in self.job_results:
			self.element = element
			self.get_job_title()
			self.get_job_company()
			self.get_job_weblink()
			self.check_if_external_link()
			if self.href_link in self.href_results:
				continue
			else:
				print("\n")
				try:
					print("Job title:", self.job_title.strip())
					print("Company:", self.job_company.strip())
					print("href_link:", self.href_link.strip())
					self.href_results.append(self.href_link.strip())
				except Exception as ex:
					print("Something went wrong", ex.__str__())


	def crawl_site(self):
		for keyword in self.keywords:
			self.keyword = keyword
			self.hexify_keyword()
			self.get_url()
			print("Scraping", self.url)
			self.get_results_page()
			self.get_soup()
			self.get_job_results()
			if self.no_result:
				##print("No more results...")
				break
			else:
				self.scrape_results()
