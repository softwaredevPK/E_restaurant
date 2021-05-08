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

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from .views import NonPublicMenuAPIView1, NonPublicMenuAPIView2,   NonPublicDishAPIView1, NonPublicDishAPIView2,\
                   NonPublicDishAPIView3, PublicMenuAPIView

urlpatterns = [
    path('nonpublic/menu/', NonPublicMenuAPIView1.as_view()),  #  add new menu, get all menus
    path('nonpublic/menu/<str:menu_name>/', NonPublicMenuAPIView2.as_view()),  # get specific menu, update it or delete
    path('nonpublic/dish/', NonPublicDishAPIView1.as_view()),  # add new dish, get all dishes
    path('nonpublic/dish/<str:menu_name>/', NonPublicDishAPIView2.as_view()),  # get all dishes for menu
    path('nonpublic/dish/<str:menu_name>/<int:dish_id>/', NonPublicDishAPIView3.as_view()),  # get specific dish, update it or delete
    path('menu/', PublicMenuAPIView.as_view()),  # get available menus
    path('docs/', include_docs_urls(title='eMenuAPI')),
    path('schema', get_schema_view(
        title='eMenuAPI',
        description='API for eMenu',
        version="1.0.0"))
]
