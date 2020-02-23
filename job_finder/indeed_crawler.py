#!/bin/python

import sys
import re
import codecs
import requests
import string
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class NoMoreResults(Exception):
   def __init__(self):
      super().__init__("No more results...")


class Indeed_Crawler:
   def __init__(self, keywords, location):
      self.homepage_url = "https://www.indeed.co.uk/"
      self.keywords = keywords.split(",")
      self.location = location
      self.headers = {
         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
         'accept-encoding': 'gzip, deflate, sdch, br',
         'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
         'Cache-Control': 'no-cache',
         'Connection': 'keep-alive'
      }

   def set_search_url(self):
      for punct in string.punctuation+" ":
         text_to_hex = "%"+codecs.encode(bytes(punct, "utf-8"), "hex").decode()
         self.keyword = self.keyword.replace(punct, text_to_hex)
      self.search_url = ''.join([
         self.homepage_url,
         "/jobs?q="+self.keyword,
         "&l="+self.location
      ])


   def send_get_request(self):
      self.response = requests.get(
         url = self.search_url,
         headers = self.headers
      )


   def set_soup(self):
      if self.response.status_code == 200:
         self.soup = BeautifulSoup(
            markup = self.response.text,
            features = "lxml"
         )
      else:
         raise NoMoreResults


   def get_job_results(self):
      self.results_section = self.soup.find("td", {"id":"resultsCol"})
      self.search_results = self.results_section.findAll(
         "div", {"class":re.compile("jobsearch-SerpJobCard.*")}
      )


   def get_title(self):
      self.title_element = self.element.find("div",{"class":"title"})
      self.title = self.title_element.text.strip()


   def get_company(self):
      company_element = self.element.find("span",{"class":"company"})
      self.company = company_element.text.strip()


   def get_href(self):
      self.href = self.title_element.a['href']

   def get_next_page(self):
      span_elements = self.soup.find_all("span",{"class":"np"})
      for span_element in span_elements:
         if span_element:
            if "Next" in span_element.text:
               a_element = span_element.parent.parent
               return a_element['href']
      raise NoMoreResults


   def check_if_external_link(self, url):
      base_url = urlparse(self.search_url).netloc
      search_protocol = urlparse(self.search_url).scheme
      if not base_url in url:
         return search_protocol+"://"+base_url+url
      else:
         return url


   def print_results(self):
      for element in self.search_results:
         self.element = element
         try:
            self.get_title()
            self.get_company()
            self.get_href()
            if self.title and self.company and self.href:
               self.href = self.check_if_external_link(url=self.href)
               print("\n")
               print("Title:", self.title)
               print("Company:", self.company)
               print("Link:", self.href)
         except Exception as ex:
            #print(ex.__str__())
            pass

   def scrape_site(self):
      for keyword in self.keywords:
         self.keyword = keyword
         print("Scraping results for", self.keyword)
         self.set_search_url()
         self.page_number = 1

         while True:
            try:
               print("\nPage {}...".format(self.page_number))
               ##get results
               self.send_get_request()
               self.set_soup()
               self.get_job_results()
               self.print_results()

               ##go to next page
               next_page_url = self.get_next_page()
               if not next_page_url:
                  raise NoMoreResults
               else:
                  urlparsed = urlparse(self.search_url)
                  self.search_url = urlparsed.scheme+"://"+urlparsed.netloc+next_page_url
                  self.page_number += 1
            except NoMoreResults:
               #print("No more results...")
               break
