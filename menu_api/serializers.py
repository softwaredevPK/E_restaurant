from rest_framework import serializers
from .models import Menu, Dish


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['name', 'description']


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['menu', 'name', 'description', 'price', 'prepare_time', 'vegetarian', 'id']
