#!/bin/python

import sys
import requests
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup 
import threading
from ni_job_crawler import NIJobsCrawl
from nijobfinder_crawler import NIJobFinderCrawl


def parse_commandline():
	parser = argparse.ArgumentParser(
		description = """Finding jobs on nijobs.com or nijobfinder.com can be a pain,
							so this script will do it for you: just give what sites you want
							to search, keywords to include, and it will return links
							to the most prevelant job postings. More site to follow."""
	)   
	parser.add_argument(
		"--job_sites", 
		help = "job sites to scrape from",
		required = True
	)

	parser.add_argument(
		"--location",
		help = "Location of job search",
		type = str
	)
	
	parser.add_argument(
		"--keywords",
		help = "keywords to search in job titles; separate with ','",
		type = str,
		required = True
	)
	
	
	parser.add_argument(
		"--apply",
		help = "",
		type = bool,
		default = False,
		required = False
	)
	
	parser.add_argument(
		"--filename",
		help = "filepath of file to transfer",
		type = str,
		required = False
	)
	return parser.parse_args()


def crawl_ni_jobs(args, threads):
	categories = {
		"Science":"26", 
		"Big Data":"117", 
		"IT":"3"
	}
	
	locations = {
		"Belfast":"23"
	}
	
	for key in categories.keys():
		category = categories[key]
		nijobs_scraper_obj = NIJobsCrawl(
			location = locations[args.location],
			category = category,
			keywords = args.keywords
		)
		thread = threading.Thread(
			name = "NI Jobs "+key+" thread",
			target = nijobs_scraper_obj.crawl_site
		)
		threads.append(thread)
		thread.start()
		print("Starting the",thread.name)


def crawl_ni_jobfinder(args, threads):
	nijobfinder_scraper_obj = NIJobFinderCrawl(
		categories = "IT|Insight & Analytics",
		location = args.location,
		keywords = args.keywords
	)
		
	thread = threading.Thread(
		name = "NI Job Finder thread",
		target = nijobfinder_scraper_obj.crawl_site
	)
	threads.append(thread)
	thread.start()
	print("Starting the",thread.name)
	




if __name__ == '__main__':
	main_threads = list()
	threads = list()
	args = parse_commandline()
	
	if args.apply:
		##do apply stuff
		pass
		
	if "ni jobs" in args.job_sites:
		main_thread = threading.Thread(
			target = crawl_ni_jobs,
			args = (args, threads)
		)
		main_threads.append(main_thread)
	if "ni jobfinder" in args.job_sites:
		main_thread = threading.Thread(
			target = crawl_ni_jobfinder,
			args = (args, threads)
		)
		main_threads.append(main_thread)
	
	for main_thread in main_threads:
		main_thread.start()
	
	
	
	

