from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import os
import time
import export_cost_structure
import standard_functions
import settings
from pynput.keyboard import Controller

# Main.py kicks off the script

settings.URL = input("What is the URL? \nPaste from 'http://' until '/action'\n")
settings.username = input("Enter the username: ")
settings.password = input("Enter the password: ")
# settings.direction = input("Would you like to Export or Import? ")
settings.cost_structure = input("Which cost structure would you like to copy? ")

# initialize keyboard controller
settings.keyboard = Controller()

# call the login function
standard_functions.login()

# Kick off process
export_cost_structure.run()

# Test #
# export_cost_structure.test()


# exit out of web browser
time.sleep(1)
settings.driver.quit()