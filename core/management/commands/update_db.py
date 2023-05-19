from django.core.management.base import BaseCommand

from core import scrapers
from core.models import Product

class Command(BaseCommand):
    help = 'Scrapes Woolworths and updates the database with the latest products'

    def handle(self, *args, **options):

        try: 
            self.stdout.write('Gathering latest woolworth products...')
            woolworths_products = scrapers.AllProductsScraper().scrape("woolworths")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"FAILED: {e}"))
            return
        self.stdout.write(self.style.SUCCESS(f"woolworth OK")) 
        self.update_database(woolworths_products)
        
        
        try: 
            self.stdout.write('Gathering latest coles products...')
            coles_products = scrapers.AllProductsScraper().scrape("coles")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"FAILED: {e}"))
            return
        self.stdout.write(self.style.SUCCESS(f"coles OK")) 
        self.update_database(coles_products)
        

        try: 
            self.stdout.write('Gathering latest aldi products...')
            aldi_products = scrapers.AllProductsScraper().scrape("aldi")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"FAILED: {e}"))
            return
        self.stdout.write(self.style.SUCCESS(f"aldi OK")) 
        self.update_database(aldi_products)
        
        
        
    def update_database(self, products):
    
        self.stdout.write('Updating database...')
        for category_name, category_products in products.items():
            for product in category_products:
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
        