#!/bin/python

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from prettytable import PrettyTable
import time


class BelfastBinCollection:
	def __init__(self, address, postcode):
		self.url = "https://dof.belfastcity.gov.uk/BinCollectionSchedulesV2/addressLookup.aspx"
		self.address = address
		self.postcode = postcode
		
	
	def open_browser(self):
		firefox_options = webdriver.FirefoxOptions()
		firefox_options.add_argument("--headless") 
		self.driver = webdriver.Firefox(
			executable_path = "/usr/bin/geckodriver",
			options = firefox_options
		) 


	def navigate_to_webform(self):
		self.driver.get(self.url)


	def send_click_to_postcode_radio_button(self):
		element = self.driver.find_element_by_xpath("//input[@id='searchBy_radio_1']")
		element.click()


	def send_text_to_search_input_field(self):
		textbox = self.driver.find_element_by_xpath("//input[@name='Postcode_textbox']")
		textbox.send_keys(self.postcode.upper())


	def click_submit_button(self):
		look_up_address = self.driver.find_element_by_name('AddressLookup_button')
		look_up_address.click()
	  
	  
	def select_address_from_drop_down_list(self):
		select = Select(self.driver.find_element_by_name("lstAddresses"))
		select.select_by_visible_text(self.address+", Belfast, "+self.postcode)
		
		
	def get_search_results(self):
		self.results = self.driver.find_elements_by_tag_name("tr") 
		
	
	def build_table_to_print_results(self):
		column_header_elements = self.results[0].find_elements_by_tag_name('th')
		column_headers = [col.text.strip() for col in column_header_elements]
		self.table_of_results = PrettyTable(column_headers)
	 
	 
	def populate_table_of_results(self):
		for result in self.results[1:]:
			results_elements = result.find_elements_by_tag_name('td')
			values = [res.text for res in results_elements]
			self.table_of_results.add_row(values)
		
	
	def scrape_bin_dates(self):
		try:
			print("Starting browser...")
			self.open_browser()
			
			print("Navigating to web form...")
			self.navigate_to_webform()
			self.send_click_to_postcode_radio_button()
			self.send_text_to_search_input_field()
			self.click_submit_button()
			
			##get results from the table
			print("Obtaining results...")
			time.sleep(2)
			self.select_address_from_drop_down_list()
			self.get_search_results()
			self.build_table_to_print_results()
			self.populate_table_of_results()			
			print (self.table_of_results)  
		except Exception as ex:
			print("Something went wrong", ex.__str__())
		finally:
			try:
				##close driver
				print("Closing browser...")
				self.driver.close()
			except:
				pass


