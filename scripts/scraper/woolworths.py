"""
Program:        Woolworths Scraper
Author:         Capstone 26 (Shey Laplanche)
Description:    This script scrapes the Woolworths website for product information.
TODO:
- Add logging
- Add error handling
- Add scraping capability for all pages in the category
- Add filtering of categories that may be temporary (e.g. "Easter")
    - This may come down to hard-coding the categories and separating the scraping of categories and products
- Add command line arguments for modes
    - Scrape all products in all categories
    - Scrape all products in a specific category
    - Scrape a specific product's details
"""

import util
from scraper import Scraper
from selenium.webdriver.common.by import By # for finding side-menu button (woolworths only)

from bs4 import BeautifulSoup 
import time

BASE_URL = "https://www.woolworths.com.au/"
EXPORT_PATH = "data/"

class WoolworthsScraper(Scraper):
    """This class is responsible for scraping the Woolworths website for product information."""
    
    def scrape_all_products(self):
        """Returns a list of all products from the Woolworths website"""
        categories = self.scrape_categories()

        for category_name, category_url in categories.items():
            products = self.scrape_products(category_url)
            util.export_products(products, category_name, export_path=EXPORT_PATH)
    
    def scrape_specific_product(self, product_code):
        """Returns a list of a specific product's details"""

        # Create URL and load page
        product_url = f"{BASE_URL}shop/productdetails/{product_code}"
        self.driver.get(product_url)

        # Create BeautifulSoup object
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # Extract product details
        product_details = {}

        # Find bottom container where product details are
        bottom_container = soup.find("div", class_="bottom-container")

        # Get "Product details" section
        description = bottom_container.find("h2", class_="product-heading").find_next().text

        # Extract data from nutrition table
        table = soup.find('div', class_='nutrition-table')
        rows = table.find_all('ul', class_='nutrition-row')
        nutrition_data = [['' for _ in range(3)] for _ in range(len(rows))]
        for i, row in enumerate(rows):
            cells = row.find_all('li', class_='nutrition-column')
            for j, cell in enumerate(cells):
                nutrition_data[i][j] = cell.text.strip()


        sections = soup.findAll("section")

        for section in sections:
            section_title_header = section.find("h3")
            if section_title_header is None: section_title = section.find("h2")
            if section_title_header is None: continue

            section_title = section_title_header.text
            
            section_content_div = section.find("div", class_="viewMore-content")
            if section_content_div is not None: section_content = section_content_div.text
            else: section_content = "NO TEXT FOUND"

            product_details[section_title] = section_content
        
        # Extract product image
        product_image_url = self.get_product_image_url(product_code)
        product_details["image_url"] = product_image_url
        product_details["nutrition_data"] = nutrition_data
        product_details["description"] = description

        return product_details


    def get_product_image_url(self, product_code, size="large"):
        if size in ["large", "medium", "small"]:
            return f"https://cdn0.woolworths.media/content/wowproductimages/{size}/{product_code}.jpg"
        else:
            return None

    
    def scrape_categories(self):
        """Returns a list of categories from the Woolworths website"""
        self.driver.get(BASE_URL)

        # This extracts the side navigation bar button by 1. The navigation bar CSS selector, 2. The button CSS selector
        btn = self.driver.find_element(By.CSS_SELECTOR, ".wx-fs-header__nav .wx-fs-header__drawer-button").click()
        time.sleep(1) # wait for menu to appear (maybe fix by stripping animation speed in CSS)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # Extract the categories and their URLs (woolworths)
        category_list_div = soup.find("div", class_="category-list")
        category_anchors = category_list_div.find_all("a", class_="item")

        # Populate categories dictionary with related links
        categories = {}
        for category_anchor in category_anchors:
            categories[category_anchor.text.strip()] = f"{BASE_URL[:-1]}{category_anchor['href']}"
        
        return categories

    def scrape_products(self, category_url):
        """Returns a list of products from a given category URL"""
        self.driver.get(category_url)
        time.sleep(3) # https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
        
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        product_tiles = soup.find_all("section", class_="product-tile-v2")
        products = []

        for product_tile in product_tiles:
            try:
                name = product_tile.find("a", class_="product-title-link").text
                price = price = product_tile.find("div", class_="product-tile-price").find("div", class_="primary").text
                link = product_tile.find("a", class_="product-title-link")["href"]
                code = link.split("/")[-2]

                # products.append([code, name, price, link])
                products.append([code, name, price]) # don't need link for now: can generate link from code

            except AttributeError:
                # product is probably out of stock - just ignore for now
                pass

            # DEBUG
            except KeyError:
                # something is wrong with the link. Lets debug
                print("Found a KeyError. Writing problem product to debug.txt")

                with open("debug.txt", "a") as file:
                    file.write(f"{str(product_tile.find('a', class_='product-title-link').text)}\n")
        
        return products