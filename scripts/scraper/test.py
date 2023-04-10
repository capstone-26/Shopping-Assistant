import woolworths

def test_scrape_all_products():
    scraper = woolworths.WoolworthsScraper()
    scraper.scrape_all_products()

def test_scrape_specific_product():
    test_product = {
        "code": "567279",
        "name": "Sealord Dory Classic Crumb Fillets 4 Pack",
        "price": "$10.50"
    }

    scraper = woolworths.WoolworthsScraper()
    product = scraper.scrape_specific_product(test_product["code"])

    print(product["description"])

def main():
    test_scrape_specific_product()
    
if __name__ == "__main__":
    main()