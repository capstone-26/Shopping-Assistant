from django.contrib import admin
from .models import Product, Watchlist, HistoricalPrice, Profile

# admin.site.register(User)
admin.site.register(Product)
admin.site.register(Watchlist)
admin.site.register(HistoricalPrice)
admin.site.register(Profile)