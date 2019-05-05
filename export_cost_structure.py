import os
import csv
import settings
import standard_functions
import time
from selenium.webdriver.support.ui import Select

# Used in case of export
output_file = []
output_dict = []
DESCRIPTION_PATH = '//*[@id="tab.costing.summary"]/form/table/tbody/tr[2]/{#arg1}/textarea'


# Navigates to the proper pages where changes are to be made / information is to be read, then kicks off the Import /
# Export function

def run():

    find_cost_structure_key()

#    navigate()

#    summary()

#    labor_costs()

#    ODC_costs()

#    indirect_costs()

#    indirect_cost_rates()


# Loops through cost structures and looks for the key associated with the name the user provides. Uses this to open the
# right page.
def find_cost_structure_key():

    webPage = settings.URL + r'/action/admin/setup/project/cost_structures/list'
    settings.driver.get(webPage)

    tbody = settings.driver.find_element_by_xpath('//*[@id="body"]/div/div[2]/table/tbody/tr/td/form/table/tbody[1]')
    trs = tbody.find_elements_by_tag_name('tr')

    for tr in trs:
        tds = tr.find_elements_by_tag_name('td')
        cost_structure_key = tr.get_attribute("id")
        if cost_structure_key.startswith("k"):
            cost_structure = tds[2].text

            if cost_structure == settings.cost_structure:
                settings.cost_structure_key = cost_structure_key.strip("k_")

    if settings.cost_structure_key == "":
        print("ERROR: Could not find cost structure")
        time.sleep(3)
        settings.driver.quit()
        exit()

def navigate():
    webPage = settings.URL + r"/action/admin/setup/project/cost_structures/list"
    settings.driver.get(webPage)

def summary():
    # Read input file specified in settings
    input_file = csv.DictReader(open(settings.summary_file))

    # Assign local variables - the value for each column in a particular row
    for row in input_file:
        cost_structure = str(row["cost_structure"])
        cost_structure_key = str(row["cost_structure_key"])
        description = str(row["description"])
        cost_pool_group = str(row["cost_pool_group"])
        active = str(row["active"])

        # If importing, proceed to import function
        if settings.direction == "Import":
            pass
        # Standard_functions.fileImport()

        # If exporting, create a dictionary containing the values from Unanet
        elif settings.direction == "Export":

            # Open cost structure Summary page
            webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit" \
                      "?costStructureSummaryKey=" + settings.cost_structure_key
            settings.driver.get(webpage)

            # Find and return cost structure name field
            xpath = '//*[@id="tab.costing.summary"]/form/table/tbody/tr[1]/td[2]/input'
            cost_structure = str(settings.driver.find_element_by_xpath(xpath).get_attribute("value"))

            # Find and return description
            xpath = '//*[@id="tab.costing.summary"]/form/table/tbody/tr[2]/td[2]/textarea'
            description = str(settings.driver.find_element_by_xpath(xpath).get_attribute("value"))

            # Assign values to row in dictionary - to be turned into output csv file
            output_dict_row = {"cost_structure": cost_structure, "cost_structure_key": cost_structure_key,
                               "description": description, "cost_pool_group": cost_pool_group, "active": active}

            # Add row to dictionary
            output_dict.append(output_dict_row)

    # Headers of export csv file
    fnames = ["cost_structure", "cost_structure_key", "description", "cost_pool_group", "active"]

    # Send completed dictionary to be exported to csv file
    standard_functions.file_export(output_dict, fnames, settings.summary_file)

    pass


def labor_costs():
    # Holds the cost structure key for URL navigation
    current_key = ""

    # Read input file specified in settings
    input_file = csv.DictReader(open(settings.labor_cost_file))

    # Determines whether or not information is being imported or exported
    if settings.direction == "Import":

        # Assign local variables - the value for each column in a particular row
        for row in input_file:
            cost_structure = str(row["cost_structure"])
            cost_structure_key = str(row["cost_structure_key"])
            cost_element = str(row["cost_element"])
            cost_element_key = str(row["cost_element_key"])

            # If new cost structure key, navigate to the correct page
            if cost_structure_key != current_key:
                # Open cost structure Summary page
                webpage = "http://sites.unanet.com/demo_jharmon/action/admin/setup/project/cost_structures/edit" \
                          "?costStructureSummaryKey=" + cost_structure_key
                settings.driver.get(webpage)

                # Click on the Labor Costs tab
                xpathId = '//*[@id="tab.costing.labor_head"]/span'
                settings.driver.find_element_by_xpath(xpathId).click()

                current_key = cost_structure_key

        pass

    elif settings.direction == "Export":

        # Go to cost structure URL
        webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit" \
                  "?costStructureSummaryKey=" + settings.cost_structure_key
        settings.driver.get(webpage)

        # Click on the Labor Costs tab
        xpathId = '//*[@id="tab.costing.labor_head"]/span'
        settings.driver.find_element_by_xpath(xpathId).click()

        # Loop through table containing cost elements, returning values to local variables.
        select = Select(settings.driver.find_element_by_name('Assigned'))
        for option in select.options:
            cost_element = option.text
            cost_element_key = option.get_attribute('value')

            # Assign values to row in dictionary - to be turned into output csv file
            output_dict_row = {"cost_structure": settings.cost_structure,
                               "cost_structure_key": settings.cost_structure_key,
                               "cost_element": cost_element, "cost_element_key": cost_element_key}
            # Add row to dictionary
            output_dict.append(output_dict_row)

    # Headers of export csv file
    fnames = ["cost_structure", "cost_structure_key", "cost_element", "cost_element_key"]

    # Send completed dictionary to be exported to csv file
    standard_functions.file_export(output_dict, fnames, settings.labor_cost_file)


def ODC_costs():
    # Holds the cost structure key for URL navigation
    current_key = ""

    # Read input file specified in settings
    input_file = csv.DictReader(open(settings.ODC_cost_file))

    # Determines whether or not information is being imported or exported
    if settings.direction == "Import":

        # Assign local variables - the value for each column in a particular row
        for row in input_file:
            cost_structure = str(row["cost_structure"])
            cost_structure_key = str(row["cost_structure_key"])
            expense_type = str(row["expense_type"])
            expense_type_key = str(row["expense_type_key"])
            cost_element = str(row["cost_element"])
            cost_element_key = str(row["cost_element_key"])

            # If new cost structure key, navigate to the correct page
            if cost_structure_key != current_key:
                # Open cost structure Summary page
                webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit" \
                          "?costStructureSummaryKey=" + cost_structure_key
                settings.driver.get(webpage)

                # Click on the Labor Costs tab
                xpathId = '//*[@id="tab.costing.labor_head"]/span'
                settings.driver.find_element_by_xpath(xpathId).click()

                current_key = cost_structure_key

        pass

    elif settings.direction == "Export":

        # Get the latest list of expense types & cost elements, return it to csv files to be referenced later
        standard_functions.get_expense_type_data()
        standard_functions.get_cost_element_data()

        # Go to cost structure URL
        webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit" \
                  "?costStructureSummaryKey=" + settings.cost_structure_key
        settings.driver.get(webpage)

        # Click on the ODC Costs tab
        xpathId = '//*[@id="tab.costing.odc_head"]'
        settings.driver.find_element_by_xpath(xpathId).click()

        # Loop through table containing cost elements, returning values to local variables.
        select = Select(settings.driver.find_element_by_name('Assigned'))
        for option in select.options:

            # keys = a combination of the expense type and cost element - split them out here
            keys = option.get_attribute('value')
            expense_type_key = keys.rsplit(";", 1)[0]
            cost_element_key = keys.rsplit(";", 1)[1]

            # search expense type DB file for key, find associated name
            expense_types_file = csv.DictReader(open(settings.expense_types_file))
            for row in expense_types_file:
                if str(row["expense_type_key"]) == expense_type_key:
                    expense_type = str(row["expense_type"])
                    break

            # search cost elements DB file for key, find associated name
            cost_elements_file = csv.DictReader(open(settings.cost_elements_file))
            for row in cost_elements_file:
                if str(row["cost_element_key"]) == cost_element_key:
                    cost_element = str(row["cost_element"])
                    break

            print(expense_type_key)
            print(expense_type)
            print(cost_element_key)
            print(cost_element)

            # Assign values to row in dictionary - to be turned into output csv file
            output_dict_row = {"cost_structure": settings.cost_structure,
                               "cost_structure_key": settings.cost_structure_key,
                               "expense_type": expense_type, "expense_type_key": expense_type_key,
                               "cost_element": cost_element, "cost_element_key": cost_element_key}

            # Add row to dictionary
            output_dict.append(output_dict_row)

    # Headers of export csv file
    fnames = ["cost_structure", "cost_structure_key", "expense_type", "expense_type_key", "cost_element",
              "cost_element_key"]

    # Send completed dictionary to be exported to csv file
    standard_functions.file_export(output_dict, fnames, settings.ODC_cost_file)


def indirect_costs():

    # Holds the cost structure key for URL navigation
    current_key = ""

    # Read input file specified in settings
    input_file = csv.DictReader(open(settings.indirect_cost_file))

    # Determines whether or not information is being imported or exported
    if settings.direction == "Import":

        # Assign local variables - the value for each column in a particular row
        for row in input_file:
            cost_structure = str(row["cost_structure"])
            cost_structure_key = str(row["cost_structure_key"])
            cost_element = str(row["cost_element"])
            cost_element_key = str(row["cost_element_key"])

            # If new cost structure key, navigate to the correct page
            if cost_structure_key != current_key:
                # Open cost structure Summary page
                webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit" \
                          "?costStructureSummaryKey=" + cost_structure_key
                settings.driver.get(webpage)

                # Click on the Labor Costs tab
                xpathId = '//*[@id="tab.costing.labor_head"]/span'
                settings.driver.find_element_by_xpath(xpathId).click()

                current_key = cost_structure_key

        pass

    elif settings.direction == "Export":

        # Go to cost structure URL
        webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit" \
                  "?costStructureSummaryKey=" + settings.cost_structure_key
        settings.driver.get(webpage)

        # Click on the Indirect Costs tab
        xpathId = '//*[@id="tab.costing.pool_head"]/span'
        settings.driver.find_element_by_xpath(xpathId).click()

        # Loop through table containing cost elements, returning values to local variables.
        tbody = settings.driver.find_element_by_xpath(
            '//*[@id="tab.costing.pool"]/form/table/tbody[1]')
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

                indirect_formula = cost_element_data[4].text

                # Assign values to row in dictionary - to be turned into output csv file
                output_dict_row = {"cost_structure": settings.cost_structure,
                                   "cost_structure_key": settings.cost_structure_key, "cost_element": cost_element,
                                   "cost_element_key": cost_element_key, "indirect_formula": indirect_formula}
                # Add row to dictionary
                output_dict.append(output_dict_row)

    # Headers of export csv file
    fnames = ["cost_structure", "cost_structure_key", "cost_element", "cost_element_key", "indirect_formula"]

    # Send completed dictionary to be exported to csv file
    standard_functions.file_export(output_dict, fnames, settings.indirect_cost_file)

    pass


def indirect_cost_rates():

    # Holds the cost structure key for URL navigation
    current_key = ""

    # Read input file specified in settings
    input_file = csv.DictReader(open(settings.indirect_cost_file))

    # Determines whether or not information is being imported or exported
    if settings.direction == "Import":

        # Assign local variables - the value for each column in a particular row
        for row in input_file:
            cost_structure = str(row["cost_structure"])
            cost_structure_key = str(row["cost_structure_key"])
            cost_element = str(row["cost_element"])
            cost_element_key = str(row["cost_element_key"])

            # If new cost structure key, navigate to the correct page
            if cost_structure_key != current_key:
                # Open cost structure Summary page
                webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit" \
                          "?costStructureSummaryKey=" + cost_structure_key
                settings.driver.get(webpage)

                # Click on the Labor Costs tab
                xpathId = '//*[@id="tab.costing.labor_head"]/span'
                settings.driver.find_element_by_xpath(xpathId).click()

                current_key = cost_structure_key

        pass

    elif settings.direction == "Export":

        fiscal_year = ""

        # Go to cost structure URL
        webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit" \
                  "?costStructureSummaryKey=" + settings.cost_structure_key
        settings.driver.get(webpage)

        # Click on the Indirect Costs tab
        xpathId = '//*[@id="tab.costing.poolRate_head"]/span'
        settings.driver.find_element_by_xpath(xpathId).click()

        # Loop through table containing rates by fiscal year / cost element
        table = settings.driver.find_element_by_xpath('//*[@id="tab.costing.poolRate"]/form/table')
        tbodys = table.find_elements_by_tag_name('tbody')

        # For each sub table (fiscal year) in the table
        for tbody in tbodys:
            fiscal_year_key = tbody.get_attribute("id")
            if fiscal_year_key.startswith("k"):

                # return the number value after "k_" as the fiscal year key for the given row
                fiscal_year_key = fiscal_year_key.strip("k_")

                #theads = tbody.find_elements_by_tag_name('thead')

                #for thead in theads:
                #    pass

                trs = tbody.find_elements_by_tag_name('tr')

                # For each row in the fiscal year
                for tr in trs:

                    rates_data = tr.find_elements_by_tag_name('td')

                    cost_element = rates_data[2].text
                    target_rate = rates_data[3].text
                    provisional_rate = rates_data[4].text
                    actual_rate = rates_data[5].text

                    cost_element_key = "1"

                    # Assign values to row in dictionary - to be turned into output csv file
                    output_dict_row = {"cost_structure": settings.cost_structure,
                                       "cost_structure_key": settings.cost_structure_key, "cost_element": cost_element,
                                       "cost_element_key": cost_element_key, "target_rate": target_rate,
                                       "provisional_rate": provisional_rate, "actual_rate": actual_rate,
                                       "fiscal_year": fiscal_year, "fiscal_year_key": fiscal_year_key}

                    # Add row to dictionary
                    output_dict.append(output_dict_row)

    # Headers of export csv file
    fnames = ["cost_structure", "cost_structure_key", "cost_element", "cost_element_key", "target_rate",
              "provisional_rate", "actual_rate", "fiscal_year", "fiscal_year_key"]

    # Send completed dictionary to be exported to csv file
    standard_functions.file_export(output_dict, fnames, settings.indirect_cost_rates_file)

    pass

## Code to add eventually ##

# xpath = '//*[@id="tab.costing.summary"]/form/table/tbody/tr[2]/td[2]/textarea'
# description = str(settings.driver.find_element_by_xpath(xpath).get_attribute("value"))

# return_value(DESCRIPTION_PATH, variable_name)
# return_value(createPath(DESCRIPTION_PATH, var, var2, var3), variable_name)
