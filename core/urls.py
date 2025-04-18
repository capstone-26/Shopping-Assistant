"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Navigable URLS: 
    path('', views.home), # Home page: where you start your journey
    path('search/', views.SearchView.as_view(), name='search'),

    path('signup/',views.SignUp,name='signup'),
    path('signin/',views.SignIn,name='signin'),
    path('signout/',views.SignOut,name='signout'),
    path('guide/', views.howtoguide,name='guide'),
    
    path('product/<str:product_id>', views.ProductView.as_view(), name='product'),
    path('productcompare/<str:product_id>/<str:viewingproduct_id>', views.CompareProductView.as_view(), name='compareProduct'),
    path('watchlists/', views.WatchlistsView.as_view(), name = 'watchlists'),
    path('watchlist/<int:watchlist_id>', views.WatchlistView.as_view(), name = 'watchlist'),
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.editProfile, name='editprofile'),
    path('addProductToWatchlist/', views.SearchView_Watchlist.as_view(), name = 'addProduct'),
    path('changepassword/', views.changepassword, name='changepassword'),

    # API/data URLs
    path('get-product-details/', views.get_product_details, name='get_product_details'),
    path('create-watchlist/', views.create_new_watchlist, name='create_watchlist'),
    path('delete-watchlist/', views.delete_watchlist, name='delete_watchlist'),
    path('watchlist/add/<int:watchlist_id>/<str:product_id>', views.add_product_to_watchlist, name='add_product_to_watchlist'),
    path('watchlist/remove/<int:watchlist_id>/<str:product_id>', views.remove_product_from_watchlist, name='remove_product_from_watchlist'),
    path('is-product-in-watchlist/<int:watchlist_id>/<str:product_id>', views.is_product_in_watchlist, name='is_product_in_watchlist'),
    path('fetch-historical-price/<str:product_id>', views.fetch_historical_price, name='fetch_historical_price'),
    path('store-historical-price/<str:product_id>', views.store_historical_price, name='store_historical_price')
]
