"""
- Parent class for scrapers to inherit from.
- Acts as a template for all scrapers in the Shopping Assistant Application
"""
import util

class Scraper:
    
    def __init__(self):
        self.driver = util.get_driver()
    
    def scrape_all_products(self):
        """Returns a list of all products from the website"""
        pass

    def scrape_specific_product(self, product_code):
        """Returns a list of a specific product's details"""
        pass

    def get_product_image_url(self, product_code, size="large"):
        """Returns a URL to a product image"""
        pass



