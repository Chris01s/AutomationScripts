import time
import pandas as pd



def convert_timestamp_to_dateformat(appointment_date,driver):
   appointment_datetime_dt = pd.Timestamp(appointment_date).to_pydatetime()
   appointment_date = appointment_datetime_dt.strftime("%m/%d/%Y")
   return appointment_date
   
def convert_datetime_to_timeformat(appointment_time):
   return appointment_time.strftime("%H:%M")

   
def select_patient_name(patient_name,driver):
   driver.find_element_by_xpath("//span[text()='Patient Detail']/../following-sibling::*").click()
   driver.find_element_by_xpath("//li[text() = '"+patient_name+"']").click()
   
   
def select_optometrist_name(optometrist_name,driver):
   driver.find_element_by_xpath("//span[text()='Optometrist Detail']/../following-sibling::*").click()
   driver.find_element_by_xpath("//li[text() = '"+optometrist_name+"']").click()

def enter_date_of_appointment(appointment_date,driver):
   driver.find_element_by_name("date").send_keys(appointment_date)
   
def enter_time_of_appointment(appointment_time,driver):
   driver.find_element_by_name("time").send_keys(appointment_time,Keys.ENTER)  
   
   
def enter_appointment_details(appointment_data,driver):
   select_patient_name(appointment_data['Patient Name'],driver)
   select_optometrist_name(appointment_data['Optometrist Name'],driver)
   
   appointment_date = convert_timestamp_to_dateformat(appointment_data['Appointment Date'],driver)
   enter_date_of_appointment(appointment_date,driver)
   
   appointment_time = convert_datetime_to_timeformat(appointment_data['Appointment Time'])
   enter_time_of_appointment(appointment_time,driver)
   print("Done with appointment detail")
