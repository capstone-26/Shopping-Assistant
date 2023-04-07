from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'address']
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description']
        
class WatchlistSerializer(serializers.ModelSerializer):
    itemCount = serializers.IntegerField()
    userID = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )
    watchlistProduct = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )
    
    class Meta:
        model = Watchlist
        fields = ['id', 'name', 'itemCount', 'userID', 'watchlistProduct']