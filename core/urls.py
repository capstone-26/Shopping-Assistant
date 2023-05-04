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
    path('profile/', views.profile),
    path('search/', views.search),
    path('watchlists/', views.Watchlists.as_view(), name = 'watchlists'),
    path('watchlists/<int:id>', views.WatchlistDetails.as_view(), name = 'watchlist-detail'),
    
    path('watchlistList/', views.watchlists, name="watchlistList"),
    path('watchlistCreate/', views.watchlistcreate, name="watchlistCreate"),
    path('watchlistUpdate/<int:id>', views.watchlistupdate, name="watchlistUpdate"),
    path('watchlistDelete/<int:id>/', views.watchlistdelete, name="watchlistDelete"),
    
    path('login/', views.login),
    path('signup/', views.signup),
    path('aboutus/', views.aboutus),
    path('product/<int:product_code_ww>', views.product),
    path('', views.home)
]
