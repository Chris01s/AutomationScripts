#!/bin/python

import selenium_classes.scraper as selenium_scraper
import requests_classes.scraper as requests_scraper
import argparse
import sys
import json


class ArgParser:
	def __init__(self):
		self.parser = argparse.ArgumentParser(
			description = """Get the tv schedule for next few hours from radio times tv guide."""
		)
		
	def add_channels(self):
		self.parser.add_argument(
			"--channels", 
			help = "channel listings to scrape",
			required = True
		)

	def add_proxies(self):
		self.parser.add_argument(
			"--add_proxies",
			help = "mask public ip, by diverting internet traffic through a proxy server",
			type = bool,
			required = False,
			default = False
		)
	
	def add_verbose(self):
		self.parser.add_argument(
			"--verbose",
			help = "Get programme description",
			type = bool,
			required = False,
			default = False
		)
		
	def get_args(self):
		self.add_channels()
		self.add_proxies()
		self.add_verbose()		




if __name__ == "__main__":
	args_obj = ArgParser()
	args_obj.get_args()
	args = args_obj.parser.parse_args()
	
	if args.verbose:
		print("Scraping with Selenium")
		scraper_obj = selenium_scraper.Scraper(
			url = "https://www.radiotimes.com/tv/tv-listings/",
			add_proxies = args.add_proxies,
			channels = args.channels.split(",")
		)
	else:
		scraper_obj = requests_scraper.Scraper(
			url = "https://www.radiotimes.com/tv/tv-listings/",
			add_proxies = args.add_proxies,
			channels = args.channels.split(",")
		)
	scraper_obj.scrape_listings()
			
	try:
		os.system("killall geckodriver")
		os.system("killall firefox")
	except:
		pass			

	
		
