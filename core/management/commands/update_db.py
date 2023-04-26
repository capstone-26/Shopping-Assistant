from django.core.management.base import BaseCommand

from core import scrapers
from core.models import Product

class Command(BaseCommand):
    help = 'Scrapes Woolworths and updates the database with the latest products'

    def handle(self, *args, **options):
        # Gather latest products
        self.stdout.write('Gathering latest products...')
        try:
            woolworths_products = scrapers.AllProductsScraper().scrape("woolworths")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"FAILED: {e}"))
            return
        
        self.stdout.write(self.style.SUCCESS(f"OK"))
        
        self.stdout.write('Updating database...')
        try:
            for category_name, category_products in woolworths_products.items():
                for product in category_products:
                    
                    Product.objects.update_or_create(
                        name = product['name'],
                        price = float(product['price'].replace("$", "")),
                        retailer = "woolworths",
                        retailer_code = product['code'],
                        category = category_name,
                    )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"There is a problem with {product['name']}"))
            self.stdout.write(self.style.ERROR(f"FAILED: {e}"))
            return
        self.stdout.write(self.style.SUCCESS("OK"))