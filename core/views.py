from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from webscraper import woolworths # for webscraping
import asyncio # for asynchronous webscraping

def home(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')

def search(request):
    return render(request, 'search.html')

class Watchlists(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'watchlists.html'

    def get(self, request):
        queryset = Watchlist.objects.all()
        return Response({'watchlists': queryset}) 

class WatchlistDetails(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'watchlistdetail.html'

    def get(self, request, id):
        watchlist = get_object_or_404(Watchlist, id=id)
        serializer = WatchlistSerializer(watchlist)
        return Response({'serializer': serializer, 'watchlist': watchlist})

@api_view(['GET'])
def watchlists(request):
    watchlists = Watchlist.objects.all()
    serializer = WatchlistSerializer(watchlists, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def watchlistcreate(request):
    serializer = WatchlistSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
@api_view(['PUT'])
def watchlistupdate(request, id):
    watchlist = Watchlist.objects.get(id=id)
    serializer = WatchlistSerializer(instance=watchlist, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)
    
@api_view(['DELETE'])
def watchlistdelete(request, id): 
    watchlist = Watchlist.objects.get(id=id)           
    watchlist.delete()
    
    return Response('Item deleted')
    
def login(request):
    return render(request, 'login.html')
def signup(request):
    return render(request, 'signup.html')
def aboutus(request):
    return render(request, 'aboutus.html')

# Testing webscraper
async def product(request, product_code_ww):

    # This subfunction is awaited on - there may be a better way to do this.
    async def scrape_product(product_code):
        return woolworths.WoolworthsScraper().scrape_specific_product(product_code)

    product = await scrape_product(product_code_ww)

    # return HttpResponse(f"Product: {str(product)}")
    return render(request, 'product.html', {'product': product})