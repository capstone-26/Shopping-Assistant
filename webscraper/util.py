from selenium import webdriver

# Using a Firefox webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
# from webdriver_manager.firefox import GeckoDriverManager

import csv
import os

# Change this to the path of the application's GeckoDriver
GECKODRIVER_PATH = "/usr/bin/geckodriver"

def get_driver():
    # Create driver
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--window-size=1920,1200") # Ensures a consistent scraping experience
    service = Service(executable_path=GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)

    return driver

def export_products(products, category_name, export_path=""):
    
    with open(f"{export_path}{category_name}.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Code", "Name", "Price"]) 
        writer.writerows(products)