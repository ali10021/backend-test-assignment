from django.http import request
from rest_framework import serializers
from accounts.serializers import UserSerializer
from sales.models import(
    SalesData,
    Country,
    City
)
from django.db import models


class SalesDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SalesData
        fields = ('id' ,'date', 'product', 'sales_number', 'revenue', 'user_id')
        
    def create(self, validated_data):
        print(self.context['request'].user)
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)
    
class CitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = City
        fields = ('id' ,'name')
    
        
class CountrySerializer(serializers.ModelSerializer):
    
    cities = CitySerializer(source='city', many=True)

    
    class Meta:
        model = Country
        fields = ('id' ,'name', 'cities')
        
