#!/bin/python

import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from openpyxl import load_workbook


def downloadRPAChallengeExcelFile():
   os.system("wget -O challenge.xlsx http://www.rpachallenge.com/challenge.xlsx")
   
def startTheChallenge():
   start_button = driver.find_element_by_id("start")
   start_button.click()
   

def submitForm():
   submit_button = driver.find_element_by_xpath("//input[@type='submit']")
   submit_button.click()
   
def getTextFieldElements():
   return driver.find_elements_by_class_name('js-inputContainer') 
   
   
def fillInTextField(element,data_point):
   element.find_element_by_class_name('form-control').send_keys(data_point)


def printResults():  
   results = driver.find_element_by_class_name('success-score').text
   print results


def cleanUpExcelFile(workbook):
   sheet = workbook['Sheet1']
   header = filter(lambda x: x!=None,[row[0].value for row in sheet.columns])
   max_cols = len(header)
   data = {}
   for i in range(max_cols):
      col = filter(lambda x: x not in (header[i],None),
                  [column[i].value for column in sheet.rows])
      data[header[i].strip()] = col
   data['Phone Number'] = [str(p) for p in data['Phone Number']]
   return data



downloadRPAChallengeExcelFile()

workbook = load_workbook('challenge.xlsx')
data = cleanUpExcelFile(workbook)
max_rows = len(data['First Name'])

##start selenium driver
driver = webdriver.Chrome() 
url = "http://rpachallenge.com/?lang=en"
driver.get(url)

startTheChallenge()

for row in range(max_rows):
   ##get all the elements containing text input fields
   elements = getTextFieldElements()
   
   ##go through each input field and enter the data
   for element in elements:
      fillInTextField(element,data[element.text][row])
   submitForm()
   

printResults()

##close driver
driver.close()
