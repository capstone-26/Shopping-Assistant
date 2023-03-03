from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')

def search(request):
    return render(request, 'search.html')

def watchlists(request):
    return render(request, 'watchlists.html')
