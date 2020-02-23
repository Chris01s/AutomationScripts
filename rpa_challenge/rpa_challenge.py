#!/bin/python

import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException 

def download_RPA_challenge_excel_file():
   os.system(
   	"wget -O challenge.xlsx http://www.rpachallenge.com/assets/downloadFiles/challenge.xlsx"
   )
   
   
def start_the_challenge(driver):
   try:
   	start_button = driver.find_element_by_xpath(
   		"//button[contains(text(),'Start')]"
   	)
   	start_button.click()
   except NoSuchElementException:
   	try:
   		start_button = driver.find_element_by_tag_name("button")
   		start_button.click()
   	except Exception as ex:
   		print("Something went wrong", ex.__str__())
   		raise Exception
 
 
def get_round_number(driver):
	round_number = driver.find_element_by_tag_name("button") 
	round_number = round_number.text.split(" ")[1].strip()
	return int(round_number)
	

def get_input_field(driver, column_name):
	anchor_element = driver.find_element_by_xpath(
		"//label[contains(text(), '" + column_name.strip() + "')]"
	)
	input_field_element = anchor_element.find_element_by_xpath(".//following::input") 
	return input_field_element
   
  
def submit_form(driver):
   submit_button = driver.find_element_by_xpath(
   	"//input[@type='submit']"
   )
   submit_button.click()
   

def fill_in_text_field(input_field_element, info):
	input_field_element.send_keys(info)


def fill_in_form(driver, data, round_number):
	for column_name in data.columns:
		##locate input field
		input_field_element = get_input_field(
			driver = driver, 
			column_name = column_name
		)
		
		##fill in field
		fill_in_text_field(
			input_field_element = input_field_element, 
			info = str(data.loc[round_number-1][column_name])
		)


def is_challenge_finished(driver):
	try:
		reset_button = driver.find_element_by_xpath(
			"//button[contains(text(),'Reset')]"
		)
		return True
	except NoSuchElementException:
		return False


def print_results(driver):  
	try:
		results = driver.find_element_by_class_name('message2').text
		print(results)
	except NoSuchElementException:
		print("finsihed")



if __name__ == '__main__':
	download_RPA_challenge_excel_file()
	
	##read in data
	data = pd.read_excel(io = 'challenge.xlsx') 
   
   ##start selenium driver
	driver = webdriver.Firefox() 
	url = "http://rpachallenge.com/?lang=en"
	
	##navigate to web page
	driver.get(url = url)

	##do challenge
	try:
		start_the_challenge(driver = driver)
		while True:
			challenge_finished = is_challenge_finished(driver = driver)
			if challenge_finished:
				break
			else:
				round_number = get_round_number(driver = driver)
				fill_in_form(
					driver = driver, 
					data = data,
					round_number = round_number
				)
				submit_form(driver = driver)
		print_results(driver = driver)
	except Exception as ex:
		print("Something went very wrong", ex.__str__())
	finally:
		##close driver
		driver.close()
		driver.quit()
