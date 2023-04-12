""" Not working... """

import woolworths

def scrape_specific_product(scraper):
    """ Currently tests Woolworths scraper. """
    product_code = 603317 # Tip-top bread
    
    print("Testing scrape_specific_product()...")
    try:
        product = scraper.scrape_specific_product(product_code)
    except Exception as e:
        print(f"FAILED: {e}")
    
    print("OK")
    return product

def create_scraper():
    print("Testing scraper initialisation...")
    try:
        scraper_ww = woolworths.WoolworthsScraper()
    except Exception as e:
        print(f"FAILED: {e}")
    
    print("OK")
    return scraper_ww

def main():
    scraper = create_scraper()
    product = scrape_specific_product(scraper)
    print(product)



    

if __name__ == "__main__":
    main()