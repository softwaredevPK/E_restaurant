"""eMenu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from .views import UnPublicMenuAPIView1, UnPublicMenuAPIView2,   UnPubliscDishAPIView1, UnPubliscDishAPIView2,\
                   UnPubliscDishAPIView3, PublicMenuAPIView

urlpatterns = [
    path('unpublic/menu/', UnPublicMenuAPIView1.as_view()),  #  add new menu, get all menus
    path('unpublic/menu/<str:menu_name>/', UnPublicMenuAPIView2.as_view()),  # get specific menu, update it or delete
    path('unpublic/dish/', UnPubliscDishAPIView1.as_view()),  # add new dish, get all dishes
    path('unpublic/dish/<str:menu_name>/', UnPubliscDishAPIView2.as_view()),  # get all dishes for menu
    path('unpublic/dish/<str:menu_name>/<int:dish_id>/', UnPubliscDishAPIView3.as_view()),  # get specific dish, update it or delete
    path('menu/', PublicMenuAPIView.as_view())
]
