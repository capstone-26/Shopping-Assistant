from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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
        wlists = Watchlist.objects.all()
        serializer = WatchlistSerializer(wlists, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST': 
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
def watchlistdetail(request):
    return render(request, 'watchlistdetail.html')
def login(request):
    return render(request, 'login.html')
def signup(request):
    return render(request, 'signup.html')
def aboutus(request):
    return render(request, 'aboutus.html')