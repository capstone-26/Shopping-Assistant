from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import logging
import pathlib


"""
CLASS:          Scraper
DESCRIPTION:    This class is responsible for creating a Selenium driver and providing 
                some common functionality to all scrapers
"""
class Scraper:

    GECKODRIVER_PATH = "/usr/bin/geckodriver"
    RETAILERS = ["woolworths","coles","aldi"]
    LOGGING_LEVEL = logging.DEBUG
    TIMEOUT = 10

    def __init__(self):
        
        # Logger will track scraping progress in Django/Docker CLI
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.LOGGING_LEVEL)
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(self.handler)

        self.driver = self._get_driver()
        self.base_url = ""
        pass

    def _get_driver(self):
        """Returns Selenium Firefox driver from installed executable"""
        self.logger.info("Creating driver...")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1200") # Ensures a consistent scraping experience

        service = Service(executable_path=self.GECKODRIVER_PATH)
        driver = webdriver.Firefox(service=service, options=options)
        self.logger.info("Driver created.")

        return driver
    
    def valid_retailer(self, retailer):
        """Returns True if the retailer is valid"""
        return retailer in self.RETAILERS
    
"""
CLASS:          AllProductsScraper
DESCRIPTION:    Scrapes additional information from a product's page that is not available in the
                retailer's browse view. This ma include description, ingredients etc.
                This is expected to be run by an AJAX call from the front-end.
"""
class ProductDetailsScraper(Scraper):
    """This class is responsible for scraping a single product from a retailer's website"""
    
    def scrape(self, product_code, retailer):
        """Returns details about a specific product"""
        if retailer is not None and not self.valid_retailer(retailer):
            raise ValueError(f"Invalid retailer: {retailer}")
    
        if retailer == "woolworths" or retailer == None:
            self.base_url = "https://www.woolworths.com.au/"
            return self._scrape_woolworths(product_code)

        elif retailer == "coles" or retailer == None:
            self.base_url = "https://shop.coles.com.au/product/"
            return self._scrape_coles(product_code)

        elif retailer == "aldi" or retailer == None:
            self.base_url = "https://www.aldi.com.au/groceries/"
            return self._scrape_aldi(product_code)


    # Scrapes details from a specific product's page 
    def _scrape_woolworths(self, product_code):
        product_url = f"{self.base_url}shop/productdetails/{product_code}"
        self.driver.get(product_url)
        
        try:
            # Wait for containing elements to load
            bottom_container = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.bottom-container")))
            product_description_div = WebDriverWait(bottom_container, self.TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//h2[@class='product-heading']/following-sibling::div")))
            product_description = product_description_div.find_element(By.CSS_SELECTOR, "div.viewMore-content").text
        except TimeoutException:
            self.logger.error(f"Timed out waiting for product details to load")
            return

        product_details = {
            "description": product_description,
        }
        
        return product_details

    # Scrapes details from a specific product's page 
    def _scrape_coles(self, product_code):
        product_url = f"{self.base_url}{product_code}"
        self.driver.get(product_url)
        try:
            # Wait for containing elements to load
            product_description = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.coles-targeting-SectionHeaderDescription"))).text
        except TimeoutException:
            self.logger.error(f"Timed out waiting for product details to load")
            return
        product_details = {
            "description": product_description,
        }
        
        return product_details
        
    # Scrapes details from a specific product's page 
    def _scrape_aldi(self, product_code):
        product_url = f"{self.base_url}{product_code}"
        self.driver.get(product_url)
        try:
            # Wait for containing elements to load
            product_description = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.detail-tabcontent"))).text
        except TimeoutException:
            self.logger.error(f"Timed out waiting for product details to load")
            return
        product_details = {
            "description": product_description,
        }
        return product_details
        
    


"""
CLASS:          AllProductsScraper
DESCRIPTION:    This class is responsible for scraping all products from the retailer's websites.
                This is expected to be run by the update_db management command.

"""
class AllProductsScraper(Scraper):
    """This class is responsible for scraping all products from a retailer's website"""

    def scrape(self, retailer = None):
        """Returns details about all products from a retailer"""
        if retailer is not None and not self.valid_retailer(retailer):
            self.logger.error(f"Invalid retailer: {retailer}")
        
        if retailer == "woolworths" or retailer == None:
            self.base_url = "https://www.woolworths.com.au/"
            return self._scrape_woolworths()
            
        if retailer == "coles" or retailer == None:
            self.base_url = "https://www.coles.com.au/browse"
            return self._scrape_coles()
        
        # TODO: Implement Aldi
        if retailer == "aldi" or retailer == None:
            self.base_url = "https://www.aldi.com.au/en/groceries/"
            return self._scrape_aldi()

        
        
    def _scrape_woolworths(self):
        """Returns details about all products from Woolworths"""
        
        # Scrape catgeories
        self.driver.get(self.base_url)
        
        # Wait for button to load
        try: 
            browse_button = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav.wx-fs-header__nav > button.wx-fs-header__drawer-button")))
        except TimeoutException:
            self.logger.error(f"Timed out waiting for browse button to load")
            return
        
        browse_button.click()

        category_list_div = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.category-list")))
        category_anchors = WebDriverWait(category_list_div, self.TIMEOUT).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.item")))
        
        categories = {} # {category_name: category_url}
        for anchor in category_anchors:
            category_name = anchor.text.strip()
            category_url = anchor.get_attribute('href')
            categories[category_name] = category_url

        all_category_products = {}

        # Scrape products in each category
        for category_name, category_url in categories.items():
            self.logger.info(f"Scraping category: {category_name}")
            category_products = []
            
            # Go to category page
            self.driver.get(category_url)

            # Wait on the price div to load
            try: 
                product_information_container = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-information-container")))
                product_tile_price = WebDriverWait(product_information_container, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-tile-price")))
                primary = WebDriverWait(product_tile_price, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.primary")))
            except TimeoutException as t_e:
                self.logger.error(f"Timed out waiting for first price div to load in category: {category_name} -> SKIPPING")
                continue # Skip this category
            
            # Wait on the product anchor to load
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
            
            all_category_products[category_name] = category_products

        return all_category_products
        
    def _scrape_coles(self):
        """Returns details about all products from coles"""
        
        # Scrape catgeories
        self.driver.get(self.base_url)
        categorie_anchors = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.coles-targeting-ShopCategoriesShopCategoryStyledCategoryContainer")))
        
        categories = {} # {category_name: category_url}
        # Iterate through each category and follow the link to get the products
        for anchor in categorie_anchors:
            # Get the link to the category page
            category_name = anchor.text.strip()
            category_url = anchor.get_attribute('href')
            # Liqour breaks more often than not and the Tobacco category has an age check so stop here
            if "tobacco" in category_url:
                break
            categories[category_name] = category_url
            
            all_category_products = {}
            
        for category_name, category_url in categories.items():
            self.logger.info(f"Scraping coles category: {category_name}")
            category_products = []
            # Go to category page
            self.driver.get(category_url)
            
            # Find all products header on the page
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
                    
            all_category_products[category_name] = category_products
            
        return all_category_products
        
    def _scrape_aldi(self):
        self.driver.get(self.base_url)
        try: 
            categorie_anchors = WebDriverWait(self.driver,self.TIMEOUT).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.productworld--list-item")))
        except TimeoutException:
            self.logger.error(f"Timed out waiting for loading categories")
            pass

        categories = {} # {category_name: category_url}
        for anchor in categorie_anchors:
        # Get the link to the category page
            category_name = anchor.find_element(By.CSS_SELECTOR, "span.ellipsis--text").text.strip()
            category_name = category_name.replace("\n…", "")
            category_url = anchor.find_element(By.CSS_SELECTOR,"a.productworld--list-item--link").get_attribute("href")
            #get rid of unnecessary categories
            if category_name != "Returns Policy" and category_name != "Fresh Produce":
                categories[category_name] = category_url
        
        all_category_products = {}
        
        for category_name, category_url in categories.items():
            self.logger.info(f"Scraping aldi category: {category_name}")
            category_products = []
            # Go to category page
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
                    # Check if the sub link to the category page is empty reload category page if its empty
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
                        try:
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
                            #skip this product if not find data
                            pass
                except TimeoutException:
                    # time out in loading product
                    pass
            
            all_category_products[category_name] = category_products
            
        return all_category_products