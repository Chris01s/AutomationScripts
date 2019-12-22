#!/bin/python

from .selenium_class import GetSelenium		
		

class TVListings(GetSelenium):
	def __init__(self, url, channels, add_proxies = False):
		super().__init__(url, add_proxies)
		self.channels = channels

	def get_channel_listing(self):
		self.channel_listing = self.driver.find_element_by_xpath(
			"//div[contains(@data-channel-name, '"+self.channel+"')]"
		)
		self.channel_listing = self.channel_listing.find_element_by_class_name(
			"programme-list"
		)
	
	def get_programme_listings(self):																
		self.programme_listings = self.channel_listing.find_elements_by_tag_name("li")
		
	def get_programme_info(self):
		self.programme_info = self.programme.get_attribute("data-hover-info")
		self.programme_info  = json.loads(self.programme_info)
	
	def get_programme_title(self):
		self.title = self.programme_info['title']
		
	def get_programme_description(self):
		self.description = self.programme_info['description']
	
	def get_start_time(self):
		self.start_time = self.programme_info['startTime']
