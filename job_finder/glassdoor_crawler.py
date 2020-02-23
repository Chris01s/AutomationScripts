#!/bin/python

import re
import sys
import codecs
import requests
import string
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class GlassdoorCrawl:
   def __init__(self, location, keywords, Apply=False):
      self.location = location
      self.keywords = keywords.split(",")
      self.Apply = Apply
      self.href_results = list()
      self.page_number = 1
      self.no_result = False
      self.search_url = "https://www.glassdoor.co.uk/Job/jobs.htm"
      self.location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"
      self.location_payload = {
         "term": self.location.strip(),
         "maxLocationsToReturn": 10
      }
      self.location_headers = {
         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
         'accept-encoding': 'gzip, deflate, sdch, br',
         'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
         'referer': 'https://www.glassdoor.co.uk/',
         'upgrade-insecure-requests': '1',
         'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
         'Cache-Control': 'no-cache',
         'Connection': 'keep-alive'
      }
      self.search_headers = {
         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'accept-encoding': 'gzip, deflate, sdch, br',
			'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
			'referer': 'https://www.glassdoor.co.uk/',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
			'Cache-Control': 'no-cache',
			'Connection': 'keep-alive'
      }


   def get_location_data(self):
      print("Getting location details...")
      self.location_response = requests.post(
         url=self.location_url,
         headers = self.location_headers,
         data = self.location_payload
      )
      if self.location_response.status_code == 200:
         self.location_data = self.location_response.json()
         self.location_id = self.location_data[0]['locationId']
         self.location_type = self.location_data[0]['locationType']
         self.search_payload = {
            'clickSource': 'searchBtn',
            'sc.keyword': self.keyword,
            'locT': self.location_type,
            'locId': self.location_id,
            'jobType': ''
         }
      else:
         print("something went wrong...{}".format)


   def get_results_page(self):
      try:
         self.result_html = requests.post(
				url = self.search_url,
				headers = self.search_headers,
            data = self.search_payload
			)
         self.next_url = self.result_html.url
         self.cookies = self.result_html.cookies
      except Exception as ex:
         print("Something went wrong",ex.__str__())


   def get_next_page(self):
      try:
         self.search_response = requests.get(
   			url = self.next_url,
   			headers = self.search_headers,
            cookies = self.cookies,
            timeout = 10
   		)
      except Exception as ex:
         print("Something went wrong",ex.__str__())


   def get_soup(self):
      if self.search_response.status_code == 200:
         self.soup = BeautifulSoup(
				markup = self.search_response.text,
				features = "lxml"
         )
      else:
         print("Something went wrong", self.search_response.status_code)


   def check_if_no_result(self):
      no_jobs_match = re.search(
         pattern = "Your search for Jobs for.*does not match any jobs\.",
         string = self.soup.text
      )
      if no_jobs_match:
         self.no_result = True
      else:
         self.no_result = False


   def get_job_results(self):
      try:
         self.job_results = self.soup.find_all(
            "li", {"class":re.compile("jl.*")}
         )
      except Exception as ex:
         print("Something went wrong",ex.__str__())


   def get_job_title(self):
      self.job_title = self.element['data-normalize-job-title'].strip()


   def get_job_company(self):
      try:
         self.job_company_element = self.element.find(
            "div", {"class":re.compile(".*jobEmpolyerName")}
         )
         self.job_company = self.job_company_element.text.strip()
      except Exception as ex:
         print("Something went wrong",ex.__str__())


   def get_job_weblink(self):
      try:
         return self.element.a['href']
      except Exception as ex:
         print("Something went wrong",ex.__str__())


   def check_if_external_link(self, href_link):
      base_url_parsed = urlparse(self.search_url)
      href_link_parsed = urlparse(href_link)
      if href_link_parsed.scheme:
         pass
      else:
         href_link = ''.join([
            base_url_parsed.scheme,
            "://",
            base_url_parsed.netloc,
            href_link
         ])
         return href_link


   def get_pagination(self):
      self.pagination = self.soup.find("div", {"class": "pagingControls"})


   def get_next_page_button(self):
         self.next_page_button = self.pagination.find("li", {"class":"next"})


   def check_if_more_results(self):
      self.get_pagination()
      if not self.pagination:
         self.no_more_results = True
      else:
         self.get_next_page_button()
         try:
            self.is_disabled = self.next_page_button.find(
               "span", {"class":"disabled"}
            )
            if self.is_disabled:
               self.no_more_results = True
            else:
               self.no_more_results = False
         except:
            self.no_more_results = True


   def get_next_page_link(self):
      return self.next_page_button.a['href']


   def scrape_results(self):
      for element in self.job_results:
         self.element = element
         self.get_job_title()
         self.get_job_company()
         href_link = self.get_job_weblink()
         href_link = self.check_if_external_link(href_link)
         if href_link in self.href_results:
            continue
         else:
            print("\n")
            try:
               print("Job title:", self.job_title.strip())
               print("Company:", self.job_company.strip())
               print("href_link:", href_link.strip())
               self.href_results.append(href_link.strip())
            except Exception as ex:
               print("Something went wrong", ex.__str__())


   def crawl_site(self):
      for keyword in self.keywords:
         self.keyword = keyword.strip()
         self.get_location_data()
         print("Scraping", self.search_url)
         self.get_results_page()
         while True:
            print("\nGetting next page...")
            self.get_next_page()
            self.get_soup()
            self.get_job_results()
            print(self.search_response.status_code)
            if self.no_result:
               print("No results...")
               break
            else:
               self.scrape_results()
               self.check_if_more_results()
               if self.no_more_results:
                  #print("No more results...")
                  break
               else:
                  next_page_link = self.get_next_page_link()
                  self.next_url = self.check_if_external_link(next_page_link)
