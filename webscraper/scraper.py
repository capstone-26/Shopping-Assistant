"""
- Parent class for scrapers to inherit from.
- Acts as a template for all scrapers in the Shopping Assistant Application
"""
import webscraper.util as util

class Scraper:
    
    def __init__(self):
        self.driver = util.get_driver()

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
    
    def scrape_all_products(self):
        """Returns a list of all products from the website"""
        pass

    async def scrape_specific_product(self, product_code):
        """Returns a list of a specific product's details"""
        pass

    async def get_product_image_url(self, product_code, size="large"):
        """Returns a URL to a product image"""
        pass



