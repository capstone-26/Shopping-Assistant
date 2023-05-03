from typing import Any, Dict
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

def home(request):
    return render(request, 'index.html')


# Please dont put unneccessary or bloaty views in here that arent being worked on. Add them when they make sense to add.


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
    

# Test Views
        
def watchlistsTest(request):
    return render(request, 'watchlists.html')

def watchlistdetailTest(request):
    return render(request, 'watchlistdetail.html')
    
class Search(ListView):
    model = Product
    template_name = 'search.html'

    def get_queryset(self):
        if self.request.GET.get('q') == None:
            object_list = Product.objects.none()
        else:
            query = self.request.GET.get('q')
            object_list = Product.objects.filter(name__icontains=query)

        return object_list