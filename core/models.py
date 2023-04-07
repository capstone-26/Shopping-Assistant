from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Retailer(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

class Location(models.Model):
    latlon = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()

class Store(models.Model):
    name = models.CharField(max_length=100)
    retailerID = models.ForeignKey(Retailer, on_delete=models.DO_NOTHING)
    location = models.OneToOneField(Location, on_delete=models.DO_NOTHING)
    product = models.ManyToManyField(Product)

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()

class Watchlist(models.Model):
    name = models.CharField(max_length=100)
    itemCount = models.IntegerField()
    userID = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    watchlistProduct = models.ManyToManyField(Product)

class UserLocation(models.Model):
    #class Meta:
    #    unique_together = (('userID', 'locationID'),)
    
    userID = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    locationID = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
