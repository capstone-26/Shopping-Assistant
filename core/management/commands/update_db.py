from django.core.management.base import BaseCommand

from core import scrapers

from core.models import Product

class Command(BaseCommand):
    help = 'Say hello to the world'

    def handle(self, *args, **options):
        # Gather latest products
        self.stdout('Gathering latest products...')
        woolworths_products = scrapers.AllProductsScraper().scrape("woolworths")
        self.stdout.write(self.style.SUCCESS("OK"))
        
        self.stdout('Updatinf database...')
        for category_name, category_products in woolworths_products.items():
            for product_details in category_products:
                Product.objects.update_or_create(
                    name=product_details["name"],
                    retailer="woolworths",
                    retailer_code=product_details["code"],
                    description=product_details["description"],
                    image_url=product_details["image_url"]
                )
        
        self.stdout.write(self.style.SUCCESS("OK"))