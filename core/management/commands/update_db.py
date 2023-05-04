from django.core.management.base import BaseCommand

from core import scrapers
from core.models import Product

class Command(BaseCommand):
    help = 'Scrapes Woolworths and updates the database with the latest products'

    def handle(self, *args, **options):

        try: 
            self.stdout.write('Gathering latest products...')
            # woolworths_products = scrapers.AllProductsScraper().scrape("woolworths")
            woolworths_products = scrapers.AllProductsScraper().scrape()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"FAILED: {e}"))
            return
        
        self.stdout.write(self.style.SUCCESS(f"OK"))        

        self.stdout.write('Updating database...')
        for category_name, category_products in woolworths_products.items():
            for product in category_products:
                try:
                    # Get existing or create new product
                    product_id = f"{product['retailer']}-{product['retailer_code']}"
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