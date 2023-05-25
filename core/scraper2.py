from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import logging
import json
import os

from core.scrapers import Scraper

class SweepingScraper(Scraper):

    EXPORT_DIRECTORY = "./core/temp/"
    PAGES_TO_SCRAPE = 2

    def scrape_woolworths(self):
        self.logger.info(f"scraping woolworth...")
        # Fixed categories and urls to scrape
        categories = {
            "Fruit & Veg": "https://www.woolworths.com.au/shop/browse/fruit-veg",
            "Bakery": "https://www.woolworths.com.au/shop/browse/bakery",
            "Lunch Box": "https://www.woolworths.com.au/shop/browse/lunch-box",
            "Meat, Seafood & Deli": "https://www.woolworths.com.au/shop/browse/meat-seafood-deli",
            "Pantry": "https://www.woolworths.com.au/shop/browse/pantry",
            "Snacks & Confectionery": "https://www.woolworths.com.au/shop/browse/snacks-confectionery",
            "Dairy, Eggs & Fridge": "https://www.woolworths.com.au/shop/browse/dairy-eggs-fridge",
            "Freezer": "https://www.woolworths.com.au/shop/browse/freezer",
            "Drinks": "https://www.woolworths.com.au/shop/browse/drinks",
            "Health & Wellness": "https://www.woolworths.com.au/shop/browse/health-wellness",
            "Beauty & Personal Care": "https://www.woolworths.com.au/shop/browse/beauty-personal-care",
            "Baby": "https://www.woolworths.com.au/shop/browse/baby",
            "Pet": "https://www.woolworths.com.au/shop/browse/pet",
            "Household": "https://www.woolworths.com.au/shop/browse/household",
            "Home & Lifestyle": "https://www.woolworths.com.au/shop/browse/home-lifestyle"
        }

        for category_name, category_url in categories.items():
            self.logger.info(f"scraping category: {category_name}")
            category_products = []

            # Now for each category, we need to scrape the specified number of pages
            for page in range(self.PAGES_TO_SCRAPE):
                self.logger.info(f" - page {page + 1}")

                category_page_url = category_url + '?pageNumber=' + str(page + 1)
                self.driver.get(category_page_url)

                # Wait on a price div to load
                try: 
                    product_information_container = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-information-container")))
                    product_tile_price = WebDriverWait(product_information_container, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-tile-price")))
                    primary = WebDriverWait(product_tile_price, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.primary")))
                except TimeoutException as t_e:
                    self.logger.error(f"Timed out waiting for first price div to load in category: {category_name} -> SKIPPING")
                    continue # Skip this category
                
                # Wait on a product anchor to load
                try: 
                    product_title_container = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-title-container")))
                    product_tile_title = WebDriverWait(product_title_container, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-tile-title")))
                    product_title_link = WebDriverWait(product_tile_title, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.product-title-link")))
                except TimeoutException as t_e:
                    self.logger.error(f"Timed out waiting for first title anchor to load in category: {category_name} -> SKIPPING")
                    continue # Skip this category

                # Find all product tiles on the page
                product_tiles = self.driver.find_elements(By.CSS_SELECTOR, "section.product-tile-v2")

                # Extract content from each of the product tiles
                for tile in product_tiles:
                    try:
                        info_container = tile.find_element(By.CSS_SELECTOR, "div.product-information-container")
                        title_container = tile.find_element(By.CSS_SELECTOR, "div.product-title-container")

                        title_anchor = title_container.find_element(By.CSS_SELECTOR, "a.product-title-link")
                        name = title_anchor.text.strip()
                        link = title_anchor.get_attribute("href")
                        price = info_container.find_element(By.CSS_SELECTOR, "div.product-tile-price").find_element(By.CSS_SELECTOR, "div.primary").text
                        retailer_code = link.split("/")[-2]

                        size = "large" # large, medium, small
                        image_url = f"https://cdn0.woolworths.media/content/wowproductimages/{size}/{str(retailer_code).zfill(6)}.jpg"

                        category_products.append({
                            "name": name,
                            "price": price if price != "" else "$0.00",
                            "retailer_code": retailer_code,
                            "category": category_name,
                            "retailer": "woolworths",
                            "image_url": image_url,
                        })
                    except NoSuchElementException as nse_e:
                        pass
                    except Exception as e:
                        self.logger.error(f"Error scraping product tile: {e}")
    
    
            # Write the products to a file
            self.export(f"woolworths-[{category_name}].json", category_products)

   
    def scrape_coles(self):
        self.logger.info(f"scraping coles...")
        categories = {
            "Meat & Seafood": "https://www.coles.com.au/browse/meat-seafood",
            "Fruit & Vegetables": "https://www.coles.com.au/browse/fruit-vegetables",
            "Dairy, Eggs & Fridge": "https://www.coles.com.au/browse/dairy-eggs-fridge",
            "Bakery": "https://www.coles.com.au/browse/bakery",
            "Deli": "https://www.coles.com.au/browse/deli",
            "Pantry": "https://www.coles.com.au/browse/pantry",
            "Drinks": "https://www.coles.com.au/browse/drinks",
            "Frozen": "https://www.coles.com.au/browse/frozen",
            "Household": "https://www.coles.com.au/browse/household",
            "Health & Beauty": "https://www.coles.com.au/browse/health-beauty",
            "Baby": "https://www.coles.com.au/browse/baby",
            "Pet": "https://www.coles.com.au/browse/pet",
        }

        for category_name, category_url in categories.items():
            self.logger.info(f"Scraping category: {category_name}")
            category_products = []

            for page in range(self.PAGES_TO_SCRAPE):
                self.logger.info(f"Scraping page: {page + 1}")

                category_page_url = f"{category_url}?page={page + 1}"
                self.driver.get(category_page_url)

                # Find all products header on the first page
                products = self.driver.find_elements(By.CSS_SELECTOR, "header.product__header")
                for product in products:
                    try:
                        name = product.find_element(By.CSS_SELECTOR, "h2.product__title").text.strip()
                        price = product.find_element(By.CSS_SELECTOR, "span.price__value").get_attribute("innerHTML")
                        productLink = product.find_element(By.CSS_SELECTOR, "a.product__link").get_attribute("href")
                        retailer_code = productLink.split("-")[-1]
                        image_url = f"https://productimages.coles.com.au/productimages/{retailer_code[0]}/{retailer_code}.jpg"

                        category_products.append({
                            "name": name,
                            "price": price,
                            "retailer_code": retailer_code,
                            "category": category_name,
                            "retailer": "coles",
                            "image_url": image_url,
                            })
                    except NoSuchElementException as nse_e:
                        pass
                    except Exception as e:
                        self.logger.error(f"Error scraping product tile: {e}")

            # Write the products to a file
            self.export(f"coles-[{category_name}].json", category_products)
            
    def scrape_aldi(self):
        self.logger.info(f"scraping aldi...")
        categories = {
            "super-savers": "https://www.aldi.com.au/en/groceries/super-savers/",
            "seasonal-range": "https://www.aldi.com.au/en/groceries/seasonal-range/",
            "Price-reductions": "https://www.aldi.com.au/en/groceries/price-reductions/",
            "dairy-eggs": "https://www.aldi.com.au/en/groceries/fresh-produce/dairy-eggs/",
            "baby": "https://www.aldi.com.au/en/groceries/baby/",
            "beauty": "https://www.aldi.com.au/en/groceries/beauty/",
            "freezer": "https://www.aldi.com.au/en/groceries/freezer/",
            "health": "https://www.aldi.com.au/en/groceries/health/",
            "laundry-household": "https://www.aldi.com.au/en/groceries/laundry-household/",
            "pantry": "https://www.aldi.com.au/en/groceries/pantry/",
        }

        for category_name, category_url in categories.items():
            self.logger.info(f"Scraping category: {category_name}")
            category_products = []
            self.driver.get(category_url)

            # Check the sub link to the category page
            sub_category_links = []
            try:
                sub_categories = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.csc-textpic-imagecolumn")))
                for sub_category in sub_categories:
                    sub_category_link = sub_category.find_element(By.XPATH, ".//a")
                    sub_category_link = sub_category_link.get_attribute("href")
                    if sub_category_link is not None and category_url in sub_category_link:
                        sub_category_links.append(sub_category_link)
            except TimeoutException:
                # no sub categories
                pass

            # Check if the sub link to the category page is empty reload category page if its empty
            if not sub_category_links:
                sub_category_links.append(category_url)
                
            for link in sub_category_links:
                self.driver.get(link)
                # Find all product data on the page
                try:
                    products = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.box--wrapper")))
                    # Extract content from each of the product tiles
                    for product in products:
                        name = product.find_element(By.CSS_SELECTOR, "div.box--description--header").text.strip()
                        value = product.find_element(By.CSS_SELECTOR, "span.box--value")
                        decimal = product.find_element(By.CSS_SELECTOR, "span.box--decimal")
                        image_url = product.find_element(By.TAG_NAME, "img").get_attribute("src")
                        product_link = product.get_attribute("href")
                        # Split the URL by "/"
                        parts = product_link.split("/")
                        # Find the index of the desired section
                        index = parts.index("groceries") + 1
                        # Join the parts starting from the groceires to make retailer_code
                        retailer_code = "/".join(parts[index:])
                        category_products.append({
                            "name": name,
                            "price": value.text.strip() + decimal.text.strip(),
                            "retailer_code": retailer_code,
                            "category": category_name,
                            "retailer": "aldi",
                            "image_url": image_url,
                        })
                except NoSuchElementException as nse_e:
                    pass
                except Exception as e:
                    self.logger.error(f"Error scraping product tile: {e}")
            
            # Write the products to a file
            self.export(f"aldi-[{category_name}].json", category_products)
        #close the driver
        self.driver.close()

    def export(self, filename, data):
        self.logger.info(f"Exporting data to {self.EXPORT_DIRECTORY}{filename}")
        with open(f"{self.EXPORT_DIRECTORY}{filename}", "w") as f:
            json.dump(data, f, indent=4)
    
    def consolidate_data(self):
        self.logger.info("Consolidating data")
        consolidated_data = []

        for filename in os.listdir(self.EXPORT_DIRECTORY):
            if filename.endswith(".json"):
                with open(f"{self.EXPORT_DIRECTORY}{filename}", "r") as f:
                    data = json.load(f)
                    consolidated_data.extend(data)

        return consolidated_data
    
    def cleanup(self):
        self.logger.info("Cleaning up")
        for filename in os.listdir(self.EXPORT_DIRECTORY):
            if filename.endswith(".json"):
                os.remove(f"{self.EXPORT_DIRECTORY}{filename}")