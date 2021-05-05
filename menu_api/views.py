from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.generics import GenericAPIView

from .serializers import DishSerializer, MenuSerializer
from .models import Menu, Dish


class PublicMenuAPIView(APIView):

    def get(self, request):
        ...


class UnPublicMenuAPIView(GenericAPIView):
    serializer_class = MenuSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_field = ['menu_name']

    def get_menu(self, menu_name):
        try:
            menu = Menu.objects.get(name=menu_name)
        except Menu.DoesNotExist:
            return None
        return menu

    def get(self, request, menu_name=None):
        if menu_name is None:
            return Response(status=status.HTTP_200_OK)
        menu = self.get_menu(menu_name)
        if menu is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(menu)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Dish Views


class BaseUnPublicDishApiView(GenericAPIView):
    serializer_class = DishSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Dish.objects.all()


class UnPubliscDishAPIView1(BaseUnPublicDishApiView):
    """
    ApiView which provide post method to create new dishes, and to show all available dishes
    """

    def get(self, request):
        dishes = Dish.objects.all()
        serializer = self.serializer_class(dishes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnPubliscDishAPIView2(BaseUnPublicDishApiView):
    """
    ApiView which provide get method to provide all dishes for given menu
    """

    def get(self, request, menu_name):
        dishes = Dish.objects.filter(menu__name=menu_name).all()
        serializer = self.serializer_class(dishes, many=True)
        return Response(serializer.data)


class UnPubliscDishAPIView3(BaseUnPublicDishApiView):
    """
    ApiView which provide get, update and delete methods for particular dish
    """

    def get_dish(self, menu_name, dish_id):
        """Method return instance of Dish or None if not exist"""
        try:
            return Dish.objects.get(menu__name=menu_name, id=dish_id)
        except Dish.DoesNotExist:
            return None

    def put(self, request, menu_name, dish_id):
        dish = self.get_dish(menu_name, dish_id)
        if dish is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(dish, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, menu_name, dish_id):
        dish = self.get_dish(menu_name, dish_id)
        if dish is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(dish)
        return Response(serializer.data)

    def delete(self, menu_name, dish_id):
        dish = self.get_dish(menu_name, dish_id)
        if dish is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        dish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)