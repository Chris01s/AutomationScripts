
def enter_optometrist_name(optometrist_name, driver):
    name_xpath = "//span[text() ='Name']/../following-sibling::*/*"
    name_input_field = driver.find_element_by_xpath(name_xpath)
    name_input_field.send_keys(optometrist_name)


def enter_optometrist_practice(optometrist_practice, driver):
    practice_name_xpath = "//span[text() ='Practice Name']/../following-sibling::*/*"
    practice_input_field = driver.find_element_by_xpath(practice_name_xpath)
    practice_input_field.send_keys(optometrist_practice)


def enter_optometrist_phone_number(optometrist_phone_number, driver):
    phone_number_xpath = "//span[text() ='Phone Number']/../following-sibling::*"
    try:
        optometrist_phone_number = str(int(optometrist_phone_number))
        phone_input_field = driver.find_element_by_xpath(phone_number_xpath)
        phone_input_field.send_keys(optometrist_phone_number)
    except ValueError:
        print "Missing data: Phone Number"


def enter_optometrist_email_address(optometrist_practice, driver):
    email_xpath = "//span[text() ='Email Address']/../following-sibling::*/*"
    email_input_field = driver.find_element_by_xpath(email_xpath)
    email_input_field.send_keys(optometrist_practice)


def enter_optometrist_details(optometrist_record, driver):
    enter_optometrist_name(optometrist_record['Optometrist Name'], driver)
    enter_optometrist_practice(optometrist_record['Practice Name'], driver)
    enter_optometrist_phone_number(optometrist_record['Optometrist Phone Number'], driver)
    enter_optometrist_email_address(optometrist_record['Email Address'], driver)
    print "Done with optometrist detail"
