from rest_framework import serializers
from .models import Menu, Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'prepare_time', 'vegetarian', 'post_date', 'update_date']


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Menu
        fields = ['name', 'description', 'post_date', 'update_date', 'dishes']


