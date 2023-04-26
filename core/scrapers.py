from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import logging 

class Scraper:

    # Installation of GeckoDriver is required for this application to work
    GECKODRIVER_PATH = "/usr/bin/geckodriver"
    RETAILERS = ["woolworths"]
    LOGGING_LEVEL = logging.DEBUG
    TIMEOUT = 10

    def __init__(self):
        # Logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.LOGGING_LEVEL)
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(self.handler)

        self.driver = self._get_driver()
        self.base_url = ""
        pass

    def _get_driver(self):
        """Returns a Selenium Firefox driver"""
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
    
class ProductDetailsScraper(Scraper):
    """This class is responsible for scraping a single product from a retailer's website"""
    
    def scrape(self, product_code, retailer):
        """Returns details about a specific product"""
        if not self.valid_retailer(retailer):
            raise ValueError(f"Invalid retailer: {retailer}")
    
        if retailer == "woolworths":
            self.base_url = "https://www.woolworths.com.au/"
            return self._scrape_woolworths(product_code)
        
    def _scrape_woolworths(self, product_code):
        product_url = f"{self.base_url}shop/productdetails/{product_code}"
        self.driver.get(product_url)
        
        try:
            product_name = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.shelfProductTile-title"))).text
            product_price = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.price"))).text.replace("\n", "").replace(" ", "")
            bottom_container = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.bottom-container")))
            product_description_div = WebDriverWait(bottom_container, self.TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//h2[@class='product-heading']/following-sibling::div")))
            product_description = product_description_div.find_element(By.CSS_SELECTOR, "div.viewMore-content").text
        except TimeoutException:
            self.logger.error(f"Timed out waiting for product details to load")
            return

        # product_name = self.driver.find_element(By.CSS_SELECTOR, "h1.shelfProductTile-title").text
        # product_price = self.driver.find_element(By.CSS_SELECTOR, "div.price price--large").text.replace("\n", "")
        
        # bottom_container = self.driver.find_element(By.CSS_SELECTOR, "div.bottom-container")
        # product_description = bottom_container.find_element(By.XPATH, "//h2[@class='product-heading']/following-sibling::div")

        size = "medium" # large, medium, small
        product_image_url = f"https://cdn0.woolworths.media/content/wowproductimages/{size}/{str(product_code).zfill(6)}.jpg"

        product_details = {
            "name": product_name,
            "price": product_price,
            "description": product_description,
            "image_url": product_image_url
        }
        
        return product_details




# To be used by management commands:
class AllProductsScraper(Scraper):
    """This class is responsible for scraping all products from a retailer's website"""

    def scrape(self, retailer):
        """Returns details about all products from a retailer"""
        if not self.valid_retailer(retailer):
            self.logger.error(f"Invalid retailer: {retailer}")
        
        if retailer == "woolworths":
            self.base_url = "https://www.woolworths.com.au/"
            return self._scrape_woolworths()
        
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
                    code = link.split("/")[-2]

                    category_products.append({
                        "name": name,
                        "price": price if price != "" else "$0.00",
                        "code": code,
                    })
                except NoSuchElementException as nse_e:
                    pass
                except Exception as e:
                    self.logger.error(f"Error scraping product tile: {e}")

            all_category_products[category_name] = category_products

        return all_category_products