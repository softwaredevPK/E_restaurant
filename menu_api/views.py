from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from django.db.models import Count

from .serializers import DishSerializer, MenuSerializer
from .models import Menu, Dish


class PublicMenuAPIView(ListAPIView):
    serializer_class = MenuSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'post_date', 'update_date', 'dish__name']
    ordering_fields = ['dish__name', 'dish_count']

    def get_queryset(self):
        return Menu.objects.filter(dish__isnull=False).annotate(dish_count=Count('dish')).distinct()


# Menu Views


class BaseUnPublicMenuApiView(GenericAPIView):
    serializer_class = MenuSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Menu.objects.all()


class UnPublicMenuAPIView1(BaseUnPublicMenuApiView):
    """
    ApiView which provide post method to create new Menu, and to show all available Menus
    """

    def get(self, request):
        user_id = request.user.id
        menus = Menu.objects.filter(user_id=user_id).all()
        serializer = self.serializer_class(menus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnPublicMenuAPIView2(BaseUnPublicMenuApiView):
    """
    ApiView which provide get, update and delete methods for particular Menu
    """

    def get_menu(self, menu_name, user_id):
        """Method return instance of Menu or None if not exist"""
        try:
            return Menu.objects.get(name=menu_name, user_id=user_id)
        except Menu.DoesNotExist:
            return None

    def put(self, request, menu_name):
        user_id = request.user.id
        menu = self.get_menu(menu_name, user_id)
        if menu is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(menu, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, menu_name):
        user_id = request.user.id
        menu = self.get_menu(menu_name, user_id)
        if menu is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(menu)
        return Response(serializer.data)

    def delete(self, request, menu_name):
        user_id = request.user.id
        menu = self.get_menu(menu_name, user_id)
        if menu is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        user_id = request.user.id
        dishes = Dish.objects.filter(menu__user__id=user_id).all()
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
        user_id = request.user.id
        dishes = Dish.objects.filter(menu__name=menu_name, menu__user__id=user_id).all()
        if dishes.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(dishes, many=True)
        return Response(serializer.data)


class UnPubliscDishAPIView3(BaseUnPublicDishApiView):
    """
    ApiView which provide get, update and delete methods for particular dish
    """

    def get_dish(self, menu_name, dish_id, user_id):
        """Method return instance of Dish or None if not exist"""
        try:
            return Dish.objects.get(menu__name=menu_name, id=dish_id, menu__user__id=user_id)
        except Dish.DoesNotExist:
            return None

    def put(self, request, menu_name, dish_id):
        user_id = request.user.id
        dish = self.get_dish(menu_name, dish_id, user_id)
        if dish is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(dish, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, menu_name, dish_id):
        user_id = request.user.id
        dish = self.get_dish(menu_name, dish_id, user_id)
        if dish is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(dish)
        return Response(serializer.data)

    def delete(self, request, menu_name, dish_id):
        user_id = request.user.id
        dish = self.get_dish(menu_name, dish_id, user_id)
        if dish is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        dish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
