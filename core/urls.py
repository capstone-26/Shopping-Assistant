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
    path('product/<str:product_id>', views.ProductView.as_view(), name='product'),
    path('watchlists/', views.WatchlistsView.as_view(), name = 'watchlists'),

    # API/data URLs
    path('get-product-details/', views.GetProductDetails, name='get_product_details'),
    path('create-watchlist/', views.CreateNewWatchlist, name='create_watchlist'),

    # path('watchlistList/', views.watchlists, name="watchlistList"),
    # path('watchlistCreate/', views.watchlistcreate, name="watchlistCreate"),
    # path('watchlistUpdate/<int:id>', views.watchlistupdate, name="watchlistUpdate"),
    # path('watchlistDelete/<int:id>/', views.watchlistdelete, name="watchlistDelete"),
    # ...

    # Testing URLs
]
