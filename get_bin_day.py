#!/bin/python

import sys
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from prettytable import PrettyTable

addressLookup = sys.argv[1]
city = sys.argv[2]
postcode = sys.argv[3]

try:
   ##open browser and got to the form web page
   driver = webdriver.Chrome() 
   url = "https://dof.belfastcity.gov.uk/BinCollectionSchedulesV2/addressLookup.aspx"
   driver.get(url)

   ##send click to POSTCODE
   element = driver.find_element_by_xpath("//input[@id='searchBy_radio_1']")
   element.click()

   ##send text to the search box
   textbox = driver.find_element_by_xpath("//input[@name='Postcode_textbox']")
   textbox.send_keys(postcode)

   ##click submit button
   look_up_address = driver.find_element_by_name('AddressLookup_button')
   look_up_address.click()

   ##select address from drop down list
   select = Select(driver.find_element_by_name("lstAddresses"))
   select.select_by_visible_text(addressLookup+", "+city+", "+postcode)

   ##get results from the table
   time.sleep(2)
   results = driver.find_elements_by_tag_name("tr") 
   column_headers = [col.text.strip() for col in results[0].find_elements_by_tag_name('th')]
   table_of_results = PrettyTable(column_headers)

   for result in results[1:]:
      values = [res.text for res in result.find_elements_by_tag_name('td')]
      table_of_results.add_row(values)
      
   print (table_of_results)  
except:
   print "Something went wrong"
finally:
   ##close driver
   driver.close()
