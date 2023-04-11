from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from webscraper import woolworths # for webscraping
import asyncio # for asynchronous webscraping

def home(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')

def search(request):
    return render(request, 'search.html')
    
@api_view(['GET', 'POST'])
def watchlists(request):
    # return render(request, 'watchlists.html')
    
    if request.method == 'GET': 
        watchlists = Watchlist.objects.all()
        serializer = WatchlistSerializer(watchlists, many=True)
        return Response(serializer.data)

    if request.method == 'POST': 
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])      
def watchlistdetail(request, id):
    # return render(request, 'watchlistdetail.html')

    try:
        watchlist = Watchlist.objects.get(pk=id)
    except Watchlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WatchlistSerializer(watchlist)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = WatchlistSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    elif request.method == 'DELETE':
        watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

def login(request):
    return render(request, 'login.html')
def signup(request):
    return render(request, 'signup.html')
def aboutus(request):
    return render(request, 'aboutus.html')

# Testing webscraper
""" 
- Currently the product is not being returned properly.
- I believe the issue is with the web scraper.
- The async part seems to be running properly though, as the page loads
"""
async def scrape_product(request):
    print("Scraping product...")
    product_code = 603317 # Tip-top bread
    wwscraper = woolworths.WoolworthsScraper()
    product = wwscraper.scrape_specific_product(product_code)

async def testscraper(request):
    product = await scrape_product(request)
    print(product)
    return HttpResponse(f"Product: {product}")