from rest_framework import serializers
from .models import Menu, Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['menu', 'name', 'description', 'price', 'prepare_time', 'vegetarian', 'id']


class MenuSerializer(serializers.ModelSerializer):
    dish_set = DishSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Menu
        fields = ['name', 'description', 'dish_set', 'user']

    def save(self, user, **kwargs):
        self.validated_data['user'] = user
        super().save()
