from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Product(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, default="DEFAULT")
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    retailer = models.CharField(max_length=100)
    retailer_code = models.CharField(max_length=150)
    description = models.TextField(default="DEFAULT")
    category = models.CharField(max_length=100, default="DEFAULT")
    image_url = models.CharField(max_length=200, default="DEFAULT")

    def __str__(self):
        return self.name

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="New Watchlist")
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.title

# class Retailer(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     url = models.URLField()

# class Location(models.Model):
#     id = models.AutoField(primary_key=True)
#     latlon = models.DecimalField(max_digits=9, decimal_places=6)
#     address = models.TextField()

# class Store(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     retailerID = models.ForeignKey(Retailer,on_delete=models.DO_NOTHING)
#     location = models.OneToOneField(Location,on_delete=models.DO_NOTHING)
#     product = models.ManyToManyField(Product)

# DEPRECATED -> User is now a built-in model
# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     address = models.TextField()

#     def __str__(self):
#         return self.name

    