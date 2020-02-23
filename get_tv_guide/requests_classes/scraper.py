#!/bin/python

from .tv_listings import TVListings
import datetime


class Scraper(TVListings):
	def __init__(self, url, channels, add_proxies):
		super().__init__(url, add_proxies)
		self.channels = channels
	
	def get_programmes(self):	
		for channel_listing in self.channel_listings:
			self.channel_listing = channel_listing
			self.get_programme_title()
			if not self.title:
				continue
			self.get_start_time()
			if not self.start_time:
				continue
			self.print_programme_info()
			
			
	def print_programme_info(self):
		print("Title:", self.title)
		print("Start time:", self.start_time)
		self.check_if_already_started()
		print("\n")
		
	def check_if_already_started(self):
		programme_time = self.start_time.replace("am", "")
		programme_time = programme_time.replace("pm", "")
		if ":" in programme_time:
			programme_time = programme_time.split(":")
			programme_time_hr, programme_time_min = programme_time
			programme_time_hr = int(programme_time_hr)
			programme_time_min = int(programme_time_min)
		else:
			programme_time_hr = int(programme_time)
			programme_time_min = 0
		
		if "pm" in self.start_time:
			programme_time_hr += 12
		
		time_now_dt = datetime.datetime.now()
		programme_time_dt = datetime.datetime(
			year = time_now_dt.year,
			month = time_now_dt.month,
			day = time_now_dt.day,
			hour = programme_time_hr,
			minute = programme_time_min
		)
		if programme_time_dt > time_now_dt:
			time_elapsed = programme_time_dt - time_now_dt
			print("Programme starts in {}".format(time_elapsed))
		else:
			time_elapsed = time_now_dt - programme_time_dt 
			print("Programme has already started: {} ago".format(time_elapsed))


	def scrape_listings(self):
		self.send_get_request()
		self.get_status_code()
		self.get_soup()
		for channel in self.channels:
			self.channel = channel.strip()
			self.get_channel_matches()
			try:
				for channel_match in self.channel_matches:
					self.channel_match = channel_match
					self.get_channel_name()
					print("\n----"+self.channel_name+"------")
					self.get_channel_listings()
					self.get_programmes()
			except:
				pass

