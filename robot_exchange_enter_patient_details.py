
import time
import pandas as pd

def convert_timestamp_to_dateformat(patient_dob,driver):
    patient_dob_dtime = pd.Timestamp(patient_dob).to_pydatetime()
    patient_dob = patient_dob.strftime("%d/%m/%Y")
    return patient_dob


def enter_patient_name(patient_name,driver):
    name_input_field = driver.find_element_by_xpath("//span[text() ='Name']/../following-sibling::*/*")
    name_input_field.send_keys(patient_name)


def enter_address_input(address_data,driver):
    address_input_field = driver.find_element_by_xpath("//label[text()='Address']/preceding-sibling::*")
    address_input_field.send_keys(address_data)


def enter_address2_input(address2_data,driver):
    try:
        address2_input_field = driver.find_element_by_xpath("//label[text()='Address 2']/preceding-sibling::*")
        address2_input_field.send_keys(address2_data)
    except:
        print "Missing data"


def enter_city_input(city_data,driver):
    try:
        city_input_field = driver.find_element_by_xpath("//label[text()='City']/preceding-sibling::*")
        city_input_field.send_keys(city_data)
    except:
        print("Missing data")


def enter_province_input(province_data,driver):
    province_input_field = driver.find_element_by_xpath("//label[text()='Province / Region']/preceding-sibling::*")
    province_input_field.send_keys(province_data)


def enter_postal_code_input(postal_code_data,driver):
    postal_code_input_field = driver.find_element_by_xpath("//label[text() ='Postal Code']/preceding-sibling::*")
    postal_code_input_field.send_keys(postal_code_data)


def enter_phone_number_input(patient_phone_number,driver):
    patient_phone_number_input_field = driver.find_element_by_xpath("//span[text() ='Phone Number']/../following-sibling::*")
    patient_phone_number_input_field.send_keys(patient_phone_number)


def enter_dob(patient_dob,driver):
    dob_input_field = driver.find_element_by_name("date")
    dob_input_field.send_keys(patient_dob)


def enter_customer_number(customer_number,driver):
    customer_number_input_field = driver.find_element_by_xpath("//span[text() ='Customer Number']/../following-sibling::*/*")
    customer_number_input_field.send_keys(customer_number)


def enter_diagnosis(diagnosis,driver):
    diagnosis_input_field = driver.find_element_by_tag_name('textarea')
    diagnosis_input_field.send_keys(diagnosis)
     


def enter_patient_details(patient_record,driver):
    enter_patient_name(patient_record['Patient Name'],driver)
    enter_address_input(patient_record['Address 1'],driver)
    enter_address2_input(patient_record['Address 2'],driver)
    enter_city_input(patient_record['City'],driver)
    enter_province_input(patient_record['County'],driver)
    enter_postal_code_input(patient_record['Postcode'],driver)
    enter_phone_number_input(patient_record['Patient Phone number'],driver)
    patient_dob = convert_timestamp_to_dateformat(patient_record['Patient DOB'],driver)
    enter_dob(patient_dob,driver)
    enter_customer_number(patient_record['Customer Number'],driver)
    enter_diagnosis(patient_record['Diagnosis or Reason for Referral'],driver)
    print("Done with patient detail")
      
   
