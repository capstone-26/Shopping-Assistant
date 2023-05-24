from typing import Any
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from core.forms import ProfileForm, UserForm
from django.contrib import messages
from .models import *
from .serializers import *
from core import scrapers
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import date

def home(request):
     
    if  request.user.is_authenticated:
            
            return render(request, 'index.html')
    else:
        return redirect(SignIn)
    
def howtoguide(request):
    return render(request, 'howto.html')
 
def SignUp(request):
    if request.method == "POST":
        name = request.POST.get('username' )
        email = request.POST.get('useremail')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 == password2:
            if User.objects.filter(username=name):
                messages.info(request,"User already exists")
                return redirect(SignUp)
            else:
                user = User.objects.create_user(username=name,password=password1,email=email)
                user.save()
                messages.success(request, f'Your account has been created. You can log in now!')
                return redirect(SignIn)
        else:
            messages.success(request, 'Password does not match!')
    return render (request,'signup.html')

def SignIn(request):
    if request.method == "POST":
        name = request.POST.get('username')
        password = request.POST.get('password')    
        user = auth.authenticate(username=name,password = password)
        if user is not None:
            auth.login(request,user)
            request.session['user'] = name
            return redirect(home)
        else:

            messages.error(request,"Invalid username or password.")
    return render(request=request, template_name="signin.html")

def SignOut(request):
    logout(request)
    print("goooddddd")
    messages.success(request, "Logged Out Successfully!!")

    return redirect(SignIn)

# Page Views
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

class SearchView_Watchlist(ListView):
    model = Product
    template_name = 'addProduct.html'

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
        context['another_value'] = self.request.GET.get('another_value')
        return context

class ProductView(View):
    model = Product
    template_name = 'product.html'

    def get(self, request, product_id):
        print(product_id)
        product = Product.objects.get(id=product_id)
        return render(request, 'product.html', {'viewingProduct': product})
    
class WatchlistsView(View):
    model = Watchlist
    template_name = 'watchlists.html'

    def get(self, request):
        user = request.user
        
        if user.is_anonymous: watchlists = []
        else:
            user_instance = User.objects.get(username=user.username)
            print(type(user_instance))
            watchlists = Watchlist.objects.filter(owner=user_instance)

        return render(request, self.template_name, {'watchlists': watchlists})

class WatchlistView(View):
    model = Watchlist
    template_name = 'watchlist.html'
    
    def get(self, request, watchlist_id):
        watchlist = Watchlist.objects.get(id=watchlist_id)

        # DEBUG
        for product in watchlist.products.all():
            print(product.name)
        
        # Ensure user owns the watchlist they are trying to view
        if request.user != watchlist.owner:
            return redirect('watchlists')

        return render(request, self.template_name, {'watchlist': watchlist})
    
class WatchlistAddProductView(View):
    model = Watchlist
    template_name = 'addProduct.html'
    
    def get(self, request, watchlist_id):
        watchlist = Watchlist.objects.get(id=watchlist_id)

        if request.user != watchlist.owner:
            return redirect('watchlists')

        return render(request, self.template_name, {'watchlist': watchlist})
    
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
        watchlists = Watchlist.objects.filter(owner=request.user)
        stop_words = set(['the', 'and', 'a', 'an', 'in', 'on', 'at', 'is', 'it', 'of', 'for','with','Woolworths', 'Coles',
                      'Aldi' 'woolworths', 'coles',
                      'aldi','No','Yes','Each','each','Pack','Pack','bottle','Bottle'])  # Define your own set of stopwords
        description = product.name
        description = description.lower()

        # Remove punctuation
        punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        description = description.translate(str.maketrans('', '', punctuation))

        # Split into words
        words = description.split()

        # Remove stopwords and words containing digits
        keywords = [word for word in words if word not in stop_words and not any(char.isdigit() for char in word)]

        combined_list = []

        for keyword in keywords:
            similar_lists = Product.objects.filter(name__icontains=keyword)
            combined_list.extend(similar_lists)

        combined_list = list(set(combined_list))  # Remove duplicate items
        
        # Retrieve historical prices
        historical_prices = HistoricalPrice.objects.filter(product=product).order_by('-date')
        
        context = {
            'viewingProduct': product,
            'watchlists': watchlists,
            'similarlists': combined_list,
            'historicalPrices': historical_prices
        }
        
        return render(request, 'product.html', context)
        
class CompareProductView(View):
    model = Product
    template_name = 'compareProduct.html'
    def get(self, request, product_id,viewingproduct_id):
        
        product = Product.objects.get(id=product_id)
        product2 = Product.objects.get(id=viewingproduct_id)
        return render(request, 'compareProduct.html', {
            'viewingProduct': product2,
            'Product': product,
             
            })
# API  or Data Views

def get_product_details(request):
    # Get product id from AJAX request
    product_id = request.POST.get('product_id')

    # Get product *retailer* id from the database
    product = Product.objects.get(id=product_id)
        
    # Scrape for product details
    scraper = scrapers.ProductDetailsScraper()
    product_details = scraper.scrape(product.retailer_code, product.retailer)

    # Update product details in database
    product.description = product_details["description"]
    product.save()

    ajax_response = {
        "description": product_details["description"],
    }

    return JsonResponse(ajax_response, status=200)

@auth.decorators.login_required
def create_new_watchlist(request):
    if request.method == 'POST':
        # Get watchlist title from AJAX request
        watchlist_title = request.POST.get('watchlist_title')
        
        # Check if watchlist title is empty
        if watchlist_title is None: 
            return JsonResponse({"error": "Watchlist title is required"}, status=400)

        # Check if user is authenticated
        if not request.user.is_authenticated: 
            return JsonResponse({"error": "User is not authenticated"}, status=401)
            
        # Create new watchlist
        user_instance = request.user

        watchlist = Watchlist.objects.create(title=watchlist_title, owner=user_instance)
        ajax_response = {
            "message": "Watchlist created successfully",
            "watchlist_id": watchlist.id,
            "watchlist_title": watchlist.title,
        }

        return JsonResponse(ajax_response, status=200)

@auth.decorators.login_required
def delete_watchlist(request):
    if request.method == 'POST':

        # Get watchlist id from AJAX request
        watchlist_id = request.POST.get('watchlist_id')

        # Check if user is authenticated
        if not request.user.is_authenticated: 
            return JsonResponse({"error": "User is not authenticated"}, status=401)

        # Check if watchlist exists
        if not Watchlist.objects.filter(id=watchlist_id).exists(): 
            return JsonResponse({"error": "Watchlist does not exist"}, status=400)
        
        # Check if user owns watchlist
        watchlist = Watchlist.objects.get(id=watchlist_id)
        if watchlist.owner != request.user:
            return JsonResponse({"error": "User does not own watchlist"}, status=401)
        
        # Delete watchlist
        watchlist.delete()

        return JsonResponse({"message": "Watchlist deleted successfully"}, status=200)

def add_product_to_watchlist(request, watchlist_id, product_id):
    watchlist = Watchlist.objects.get(id=watchlist_id)
    product = Product.objects.get(id=product_id)

    response = {
        "message": "",
        "error": "",
        "productAlreadyAdded": False
    }
    status = 200

    # Check if user is authenticated
    if not request.user.is_authenticated:
        response["error"] = "User is not authenticated"
        status = 401

    # Check if user owns watchlist
    if request.user != watchlist.owner:
        response["error"] = "User does not own watchlist"
        status = 401

    # Check if product is already in watchlist
    if product in watchlist.products.all():
        response["message"] = "Product already in watchlist"
        response["productAlreadyAdded"] = True
    else:
        watchlist.products.add(product)
        response["message"] = "Product added to watchlist"
    
    return JsonResponse(response, status=status)

def remove_product_from_watchlist(request, watchlist_id, product_id):
    if request.method == 'POST':
        watchlist_id = request.POST.get('watchlist_id')
        product_id = request.POST.get('product_id')
        try:
            watchlist = Watchlist.objects.get(id=watchlist_id)
            watchlist.products.remove(product_id)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def is_product_in_watchlist(request, watchlist_id, product_id):
    if request.method == 'POST':
        watchlist_id = request.POST.get('watchlist_id')
        product_id = request.POST.get('product_id')
        try:
            print(f"watchlist_id: {watchlist_id}\n product_id: {product_id}")
            watchlist = Watchlist.objects.get(id=watchlist_id)
            product = Product.objects.get(id=product_id)
            
            if product in watchlist.products.all():
                return JsonResponse({'status': True})
            else:
                return JsonResponse({'status': False})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
# User Profile views

def profile(request):
    User = request.user
    return render(request, 'profile.html', {'user': User})

@login_required(login_url='signin/')
@transaction.atomic
def editProfile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, (
                'Your profile was successfully updated!'))
            return redirect('/profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'editprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# Historical Price views

def historical_price(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    historicalPrices = HistoricalPrice.objects.filter(product=product).order_by('-date')
    context = {
        'productName': product,
        'historicalPrices': historicalPrices
    }
    return render(request, 'product.html', context)

def store_historical_price(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    current_price = product.price
    
    status = 200

    latest_price_entry = HistoricalPrice.objects.filter(product=product).order_by('-date').first()

    # Check if new price is different to existing price
    if latest_price_entry is None or latest_price_entry.price != current_price:
        historical_price = HistoricalPrice(product=product, price=current_price, date=date.today())
        historical_price.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})













