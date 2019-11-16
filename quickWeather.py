import json
import requests
import sys
from prettytable import PrettyTable
import argparse


def parse_commandline():
	parser = argparse.ArgumentParser(
		description = """Produces a 5-day forecast for every 3-hrs"""
	)   

	parser.add_argument(
		"--location", 
		help = "Enter a city name",
		type = str,
		required = True
	)

	parser.add_argument(
		"--appid_key",
		help = "api-key for your open weather api account",
		type = str,
		required = True
	)

	return parser.parse_args()


def send_api_request(location, appid_key):
	#: download json data from openweathermap.org api
	headers = {
		"Content-Type": 'text/css; charset=utf-8',
		"Accept": 'text/css,json,*/*;q=0.1',
		"User-Agent":'Mozilla/5.0 (X11; Linux x86_64)'
						' AppleWebKit/537.36 (KHTML, like Gecko) '
						' snap Chromium/78.0.3904.97 Chrome/78.0.3904.97 Safari/537.36'
	}
	url = "https://api.openweathermap.org/data/2.5/forecast?q=%s&APPID=%s"%(location,appid_key)
	print("Sending request...")
	response = requests.get(
		url = url,
		headers = headers
	)
	print("Received response", response.status_code)
	return response


	
 
 
def get_weather_data(response):
	try:
		return response.json()
	except Exception as ex:
		print("Something went wrong", ex.__str__())
			


def get_date(element):
	try:
		return element['dt_txt'] 
	except:
		return "could not retreive"



def get_temperature(element):
	try:
		return element['main']['temp'] - 273.15 
	except:
		return "could not retreive"
	
	

def get_weather_description(element):
	try:
		return element['weather'][0]['description']
	except:
		return "could not retreive"



def get_cloud_coverage(element):
	try:
		return element['clouds']['all'] 
	except:
		return "could not retreive"
		
		
		
def build_table_for_forecast():
	forecast_table = PrettyTable([
		"date", "weather", "temperature", "cloud coverage(%)"
	])
	return forecast_table


def get_weather_results(weather_data):
	forecast_table = build_table_for_forecast()
	try:
		for element in weather_data['list']: 
			date = get_date(element)
			temperature = get_temperature(element)
			weather =  get_weather_description(element)
			cloud_percentage = get_cloud_coverage(element)
			forecast_table.add_row([ 
				date, weather, temperature, cloud_percentage 
			]) 
		return forecast_table
	except:
		return weather_data
	
 



if __name__ == '__main__':
	args = parse_commandline()
	location = args.location
	appid_key = args.appid_key


	#: send request to openweather api
	response = send_api_request(location, appid_key)

	#: load json data into python variable
	weather_data = get_weather_data(response)

	#print weather desc for the next three days
	weather_forecast = get_weather_results(weather_data)
	print(weather_forecast)

