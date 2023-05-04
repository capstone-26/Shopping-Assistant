from typing import Any
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from core import scrapers

def home(request):
    return render(request, 'index.html')


# Please dont put unneccessary or bloaty views in here that arent being worked on. Add them when they make sense to add.

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


class SearchView(ListView):
    model = Product
    template_name = 'search.html'

    def get_queryset(self):
        if self.request.GET.get('q') == None:
            object_list = Product.objects.none()
        else:
            query = self.request.GET.get('q')
            object_list = Product.objects.filter(name__icontains=query)

        return object_list

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

class ProductView(View):
    model = Product
    template_name = 'product.html'

    def get(self, request, product_id):
        print(product_id)
        product = Product.objects.get(id=product_id)
        return render(request, 'product.html', {'product': product})
    
def GetProductDetails(request):

    # Get product id from AJAX request
    product_id = request.POST.get('product_id')

    # Get product *retailer* id from the database
    product = Product.objects.get(id=product_id)
        
    # Scrape for product details
    scraper = scrapers.ProductDetailsScraper()
    product_details = scraper.scrape(product.retailer_code, product.retailer)

    ajax_response = {
        "description": product_details["description"],
        "image_url": product_details["image_url"],
    }

    return JsonResponse(ajax_response, status=200)

# Test Views