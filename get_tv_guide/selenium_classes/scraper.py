#!/bin/python

from .tv_listings import TVListings

	
class Scraper(TVListings):
	def __init__(self, url, channels, add_proxies):
		super().__init__(url, channels, add_proxies)

	def check_if_already_started(self):
		programme_time = self.start_time.replace("am", "")
		programme_time = programme_time_dt.replace("pm", "")
		programme_time = programme_time.split(":")
		programme_time_hr, programme_time_min = programme_time
		time_now_dt = datetime.datetime.now()
		programme_time_dt = datetime.datetime(
			year = time_now_dt.year,
			month = time_now_dt.month,
			day = time_now_dt.day,
			hour = int(programme_time_hr),
			minute = int(programme_time_min)
		)
		time_elapsed = time_now_dt - programme_time_dt
		print("Programme starts in {}".format(time_elapsed))
	
	def get_programmes(self):
		for programme in self.programme_listings:
			self.programme = programme
			self.get_programme_info()
			self.get_programme_title()
			self.get_programme_description()
			self.get_start_time()
			self.print_programme_info()
		
	def print_programme_info(self):
		print("Title:", self.title)
		print("Description:", self.description)
		print("Start time:", self.start_time)
		self.check_if_already_started()
		print("\n")
	
	def get_tv_listings(self):
		for channel in self.channels:
			self.channel = channel.strip()
			print(self.channel)
			try:
				self.get_channel_listing()
				print("Found channel listing...")
				self.get_programme_listings()
				print("Found programmes")
				self.get_programmes()
			except Exception as ex:
				print("Something went wrong", ex.__str__())
			
			
	def scrape_listings(self):
		self.get_firefox_driver()
		self.start_driver()
		self.retrieve_status_code()
		if self.status_code != 200:
			print("Something went wrong", self.status_code)
			self.close_driver()
			sys.exit()
		else:
			self.get_tv_listings()
			self.close_driver()
