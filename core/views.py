from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')

def search(request):
    return render(request, 'search.html')

def watchlists(request):
    return render(request, 'watchlists.html')

def watchlistdetail(request):
    return render(request, 'watchlistdetail.html')
def login(request):
    return render(request, 'login.html')
def signup(request):
    return render(request, 'signup.html')
def aboutus(request):
    return render(request, 'aboutus.html')