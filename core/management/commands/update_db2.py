from django.core.management.base import BaseCommand

from core import scraper2
from core.models import Product

class Command(BaseCommand):
    help = 'Scrapes Woolworths and updates the database with the latest products'

    def handle(self, *args, **options):
        
        scraper = scraper2.SweepingScraper()

        self.stdout.write('Scraping data...')
        try:
            # Scrape all data to core/temp/
            scraper.scrape_woolworths()
            scraper.scrape_coles()
            scraper.scrape_aldi()
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"FAILED: {e}"))
            return
    
        # Read the files just scraped and consolidate them into a single list
        self.stdout.write('Consolidating Data...')
        products = scraper.consolidate_data()

        # Load them into the database
        self.stdout.write('Updating database...')
        self.update_database(products)

        # Delete the files
        scraper.cleanup()
        # TODO: Test this function
        
        
    def update_database(self, products):
    
        for product in products:
            try:
                # Get existing or create new product
                # !!! replace for aldi issue
                replace = product['retailer_code'].replace("/", "")
                product_id = f"{product['retailer']}-{replace}"
                product_obj = Product.objects.filter(id=product_id).first() or Product(id=product_id)

                # Update product fields
                product_obj.name = product['name']
                product_obj.price = float(product['price'].replace("$", ""))
                product_obj.retailer = product['retailer']
                product_obj.retailer_code = product['retailer_code']
                product_obj.category = product['category']
                product_obj.image_url = product['image_url']

                # Save product
                product_obj.save()

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"There is a problem with {product['name']}"))
                self.stdout.write(self.style.ERROR(f"FAILED: {product[e]}"))
                pass
        self.stdout.write(self.style.SUCCESS("OK"))
        