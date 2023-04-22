from django.core.management.base import BaseCommand

from webscraper import woolworths

class Command(BaseCommand):
    helo = 'Say hello to the world'

    def handle(self, *args, **options):
        # Gather latest products
        scraper = woolworths.WoolworthsScraper()
        products = scraper.scrape_all_products()

        # Unpack data and insert into database