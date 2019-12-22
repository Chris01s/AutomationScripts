#!/bin/python

import re
from .get_soup import GetSoup
	
class TVListings(GetSoup):
	def get_channel_matches(self):
		self.channel_matches = self.soup.find_all(
			"div", {"data-channel-name":re.compile(self.channel+".*")}
		)
		
		
	def get_channel_name(self):
		self.channel_name = self.channel_match.attrs['data-channel-name']
		self.channel_name = self.channel_name.strip()
		
		
	def get_channel_listings(self):
		self.channel_listings = self.channel_match.find_all("li")
		
		
	def get_programme_title(self):
		try:
			self.title = self.channel_listing.find(
				"span", {"class":"title-inner"}
			)
			self.title = self.title.text.strip()
		except:
			pass
		
			
	def get_start_time(self):
		try:
			self.start_time = self.channel_listing.find(
				"span", {"class":"programme-time"}
			)
			self.start_time = self.start_time.text.strip()
		except:
			pass
