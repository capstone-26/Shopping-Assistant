from django.core.management.base import BaseCommand

from core.models import Product

class Command(BaseCommand):

    def handle(self, *args, **options):

        self.stdout.write('Updating category...')
        affected_objects = Product.objects.filter(category = "DEFAULT").update(category = "")
        self.stdout.write(self.style.SUCCESS("OK"))

        self.stdout.write('Updating description...')
        affected_objects = Product.objects.filter(description = "DEFAULT").update(description = "")
        self.stdout.write(self.style.SUCCESS("OK"))

        self.stdout.write('Updating image_url...')
        affected_objects = Product.objects.filter(image_url = "DEFAULT").update(image_url = "")
        self.stdout.write(self.style.SUCCESS("OK"))

        self.stdout.write('Updating name...')
        affected_objects = Product.objects.filter(name = "DEFAULT").update(name = "")
        self.stdout.write(self.style.SUCCESS("OK"))