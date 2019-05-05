import csv
import settings
from selenium import webdriver
from pathlib import Path

home = str(Path.home())


# starts google chrome in either headless (export) or standard (import) mode.

def initialize_browser():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": r"C:\Users\jharmon\Downloads"}
    chromeOptions.add_experimental_option("prefs", prefs)
    # chromeOptions.add_argument("--headless")
    chromeDriver = r"C:\Users\jharmon\drivers\chromedriver.exe"
    settings.driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chromeOptions)


# logs into the browser with credentials provided in settings.py

def login():
    initialize_browser()

    settings.driver.get(settings.URL + "/action/home")

    id_box = settings.driver.find_element_by_name('username')
    id_box.send_keys(settings.username)

    pass_box = settings.driver.find_element_by_name('password')
    pass_box.send_keys(settings.password)

    login_button = settings.driver.find_element_by_name('button_ok')
    login_button.click()


def file_export(output_dict, fnames, file):
    # Take file, open as writable, and pass through the output dictionary.
    with open(file, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=fnames, lineterminator='\n')
        dict_writer.writeheader()
        dict_writer.writerows(output_dict)

        output_dict.clear()


def get_expense_type_data():
    output_dict = []
    fnames = ["expense_type", "expense_type_key"]

    # Navigate to expense type setup page
    webpage = settings.URL + r"/action/admin/setup/expense/expense_types/list"
    settings.driver.get(webpage)

    # Find table containing all expense type
    tbody = settings.driver.find_element_by_xpath('//*[@id="body"]/div/div[2]/table/tbody/tr[2]/td/form/table/tbody[1]')
    tbody_rows = tbody.find_elements_by_tag_name('tr')

    # For each row in the table, check if it contains a key (strip out blank rows)
    for tbody_row in tbody_rows:
        expense_type_key = tbody_row.get_attribute("id")
        if expense_type_key.startswith("k"):
            # return the number value after "k_" as the expense type key for the given row
            expense_type_key = expense_type_key.strip("k_")
            expense_type_data = tbody_row.find_elements_by_tag_name('td')

            # return the 5th attribute of that row, the expense type code.
            # 4th is name / 6th is wizard / 7th is description / 8th is cost account
            expense_type = expense_type_data[4].text

            # Assign values to row in dictionary - to be turned into output csv file
            output_dict_row = {"expense_type": expense_type, "expense_type_key": expense_type_key}
            # Add row to dictionary
            output_dict.append(output_dict_row)

    file_export(output_dict, fnames, settings.expense_types_file)

    output_dict.clear()


def get_cost_element_data():

    output_dict = []
    fnames = ["cost_element", "cost_element_key"]

    # Navigate to cost element setup page
    webpage = settings.URL + r"/action/admin/setup/project/cost_element/list"
    settings.driver.get(webpage)

    # Find table containing all cost elements
    tbody = settings.driver.find_element_by_xpath('//*[@id="body"]/div/div[2]/table/tbody/tr[2]/td/form/table/tbody[1]')
    tbody_rows = tbody.find_elements_by_tag_name('tr')

    # For each row in the table, check if it contains a key (strip out blank rows)
    for tbody_row in tbody_rows:
        cost_element_key = tbody_row.get_attribute("id")
        if cost_element_key.startswith("k"):
            # return the number value after "k_" as the cost element key for the given row
            cost_element_key = cost_element_key.strip("k_")

            # return the 4th attribute of that row, the cost element code.
            cost_element_data = tbody_row.find_elements_by_tag_name('td')
            cost_element = cost_element_data[3].text

            # print(cost_element_key)
            # print(cost_element)

            # Assign values to row in dictionary - to be turned into output csv file
            output_dict_row = {"cost_element": cost_element, "cost_element_key": cost_element_key}
            # Add row to dictionary
            output_dict.append(output_dict_row)

    file_export(output_dict, fnames, settings.cost_elements_file)

    output_dict.clear()