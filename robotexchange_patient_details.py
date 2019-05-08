#!/bin/python

import os
import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotVisibleException
import robot_exchange_enter_patient_details as robot_patients
import robot_exchange_enter_optometrist_details as robot_optometrists
import robot_exchange_enter_appointment_details as robot_appointments



def get_header_h2():
   return driver.find_element_by_tag_name('h2').text

 
def submit_details():
   driver.find_element_by_xpath('//button[@type = "submit"]').click()
   

def refresh_add_patient_detail_form():
   time.sleep(1)
   driver.find_element_by_xpath("//span[text() = 'Reload form']")
   

def get_message_warning():
   return driver.find_element_by_tag_name("strong").text
   

def click_patient_details_tab():
   add_patient_details_btn = driver.find_element_by_xpath("//span[text() = 'Patient Details']")
   add_patient_details_btn.click()


def click_add_patient_detail_btn():
   add_patient_detail_btn = driver.find_element_by_xpath("//span[text() = 'Add Patient Detail']")
   add_patient_detail_btn.click()
   
   
def click_optometrist_details_tab():
   driver.find_element_by_xpath("//span[text() = 'Optometrist Details']/../*").click()
   

def click_add_optometrist_detail_btn():
   driver.find_element_by_xpath("//span[text() = 'Add Optometrist Detail']").click()
   
   
def click_appointment_details_tab():
   driver.find_element_by_xpath("//span[text() = 'Appointment Details']/../*").click()
   

def click_add_appointnment_detail_btn():
   driver.find_element_by_xpath("//span[text() = 'Add Appointment Detail']").click()
   
   
   
if __name__ == '__main__':
   
   driver = webdriver.Chrome() 
   url = "https://robotexchange.knack.com/appointment#patient-details/"
   driver.get(url)
   time.sleep(2)
   filepath = sys.argv[1]
   appointment_data = pd.read_excel(filepath)
   
   
   for row_index in appointment_data.index:
      time.sleep(0.5)
      patient_record = appointment_data.loc[row_index]
      
      ##fill out patient details
      click_add_patient_detail_btn()
      header = get_header_h2()
      if header == "Add Patient Detail":
         robot_patients.enter_patient_details(patient_record,driver)
         submit_details()
         time.sleep(1)
         try:
            refresh_add_patient_detail_form()
            time.sleep(1)
         except ElementNotVisibleException:
            print(get_message_warning())
            click_patient_details_tab()
            continue
      
      
      ##fill out optometrist details
      click_optometrist_details_tab()
      time.sleep(2)
      header = get_header_h2()
      if header == "Optometrist Details":
         click_add_optometrist_detail_btn()
      header = get_header_h2()
      if header == "Add Optometrist Detail":
         try:
            robot_optometrists.enter_optometrist_details(patient_record,driver)
            submit_details()
         except:
            print("something went wrong")
            
       
      
      ##fill out appointment details
      click_appointment_details_tab()
      time.sleep(1)
      click_add_appointnment_detail_btn()
      time.sleep(1)
      header = get_header_h2()
      if header == "Add Appointment Detail":
         try:
            robot_appointments.enter_appointment_details(patient_record,driver)
         except:
            print("Something went wrong")
            
      click_patient_details_tab()
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
