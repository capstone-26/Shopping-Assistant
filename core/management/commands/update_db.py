from django.core.management.base import BaseCommand

from webscraper import woolworths

class Command(BaseCommand):
    helo = 'Say hello to the world'

    def handle(self, *args, **options):
        # Gather latest products
        scraper = woolworths.WoolworthsScraper()
        products = scraper.scrape_all_products()
        
        """
        This is the format of the products variable (dict):
        {
            'Fruit & Veg': [
                ['663734', 'The Salad Servers Turmeric Cauliflower & Cranberry Salad 300g', '$6.30'], 
                ['839321', 'The Salad Servers Salad Bean Medley 300g', '$6.30'], 
                ['11358', 'The Salad Servers Lentil Salad 800g', '$10.50'],
                ...
            ]
        }
        """

        # Unpack data and insert into database
        # ... here is the code that will insert shit into the db