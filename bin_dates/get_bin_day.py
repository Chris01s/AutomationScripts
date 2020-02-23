#!/bin/python

import argparse
from belfast_class import BelfastBinCollection
from lisburn_class import LisburnBinCollections

def parse_commandline():
	parser = argparse.ArgumentParser(
		description = """Search for bin collection day in the belfast council area"""
	)   
	parser.add_argument(
		"--address", 
		help = "job sites to scrape from",
		required = True
	)

	parser.add_argument(
		"--city",
		help = "Location of job search",
		type = str
	)
	
	parser.add_argument(
		"--postcode",
		help = "keywords to search in job titles; separate with ','",
		type = str,
		required = True
	)
	return parser.parse_args()
	
	
	
if __name__ == '__main__':
	args = parse_commandline()
	
	addressLookup = args.address.strip()
	city = args.city.strip()
	postcode = args.postcode.strip().upper()

	if "Lisburn" in city:
		scraper_obj = LisburnBinCollections(addressLookup, postcode)
		scraper_obj.scrape_bin_dates()
	elif "Belfast" in city:
		scraper_obj = BelfastBinCollection(addressLookup, postcode)
		scraper_obj.scrape_bin_dates()
	else:
		os.system("python get_bin_day.py -h")

