#!/bin/python


from selenium import webdriver
from selenium.webdriver.support.ui import Select

##open browser and got to the form web page
driver = webdriver.Chrome() 
url = "https://dof.belfastcity.gov.uk/BinCollectionSchedulesV2/addressLookup.aspx"
driver.get(url)

##send click to POSTCODE
element = driver.find_element_by_xpath("//input[@id='searchBy_radio_1']")
element.click()

##send text to the search box
textbox = driver.find_element_by_xpath("//input[@name='Postcode_textbox']")
textbox.send_keys("BT9 7AY")

##click submit button
look_up_address = driver.find_element_by_name('AddressLookup_button')
look_up_address.click()

##select address from drop down list
select = Select(driver.find_element_by_name("lstAddresses"))
select.select_by_visible_text('Apartment 2,2A Dunluce Avenue, Belfast, BT9 7AY')

##get results from the table
results = driver.find_element_by_id("binsGrid") 
columns = results.find_elements_by_tag_name('th') 
values = results.find_elements_by_tag_name('td') 

##print results
for col,val in zip(columns,values):
   print col.text+":",val.text
   
##close driver
driver.close()
