from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from django.urls import include, path, reverse

import datetime
import json

from .models import Dish, Menu


class UnAuthenticatedTestCase(APITestCase):
    """Testing API for UnAuthanticated user"""

    unpublic_urls = ['/unpublic/menu/', '/unpublic/menu/menu/', '/unpublic/dish/', '/unpublic/dish/dish_name/', '/unpublic/dish/dish_name/1/']

    def test_public_access(self):
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unpublic_access(self):
        for url in self.unpublic_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedTestCase2(APITestCase):
    """Testing API for Authanticated user"""

    urls_200 = ['/unpublic/menu/', '/unpublic/dish/',]

    urls_404 = ['/unpublic/menu/menu/', '/unpublic/dish/dish_name/', '/unpublic/dish/dish_name/1/']

    def setUp(self):
        self.user = User.objects.create_user(username='Leonardo', password='Da-vinci')
        self.user2 = User.objects.create_user(username='John', password='Bravo')

    def test_public_access(self):
        self.client.force_login(self.user)
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unpublic_access(self):
        self.client.force_login(self.user)
        for url in self.urls_404:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        for url in self.urls_200:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_menu_get(self):
        empty_menu = Menu.objects.create(name='Test name 2', description='Test description', user=self.user)
        menu = Menu.objects.create(name='Test name 1', description='Test description', user=self.user)
        Dish.objects.create(name='Test dish 1', description='Test description', price=10, prepare_time=datetime.timedelta(days=0, seconds=600), menu=menu)
        Dish.objects.create(name='Test dish', description='Test description', price=10,
                            prepare_time=datetime.timedelta(days=0, seconds=800), menu=menu)
        response = self.client.get('/menu/')
        self.assertEqual(len(response.data), 1)  # check if return menus which contains dishes only
        self.assertEqual(response.data[0]['name'], 'Test name 1')  # check if correct menu was returned

        # sorting + ordering
        response = self.client.get('/menu/?search=dish+2')
        self.assertEqual(response.data[0]['name'], 'Test name 1')  # check if correct menu was returned

        Dish.objects.create(name='1 dish', description='Test description', price=10,
                            prepare_time=datetime.timedelta(days=0, seconds=800), menu=empty_menu)
        response = self.client.get('/menu/?ordering=dish_count')  # ascending
        self.assertEqual(response.data[0]['dish_set'][0]['name'], '1 dish')  # check order of dishes

    def test_unpublic_menu_get(self):
        self.client.force_login(self.user)
        Menu.objects.create(name='name1', description='Test description', user=self.user)
        Menu.objects.create(name='name2', description='Test description', user=self.user2)
        response = self.client.get('/unpublic/menu/')
        self.assertEqual(len(response.data), 1)

        response = self.client.get('/unpublic/menu/name1/')
        self.assertEqual(response.data['name'], 'name1')

        response = self.client.get('/unpublic/menu/name2/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unpublic_menu_post(self):
        self.client.force_login(self.user)
        data = {'name': 'test name', 'description': 'description', 'user': self.user}
        response = self.client.post('/unpublic/menu/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'test name')
        self.assertEqual(response.data['description'], 'description')

    def test_unpublic_menu_delete(self):
        self.client.force_login(self.user)
        Menu.objects.create(name='menu1', description='Test description', user=self.user)
        response = self.client.delete(f'/unpublic/menu/menu1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 0)

    def test_unpublic_menu_put(self):
        self.client.force_login(self.user)
        menu1 = Menu.objects.create(name='menu1', description='Test description', user=self.user)
        response = self.client.put(f'/unpublic/menu/menu1/',
                                   data={'name': 'menu1', 'description': 'Updated description'})
        self.assertEqual(response.data['description'], 'Updated description')

    def test_unpublic_dish_get(self):
        self.client.force_login(self.user)
        menu1 = Menu.objects.create(name='menu1', description='Test description', user=self.user)
        menu2 = Menu.objects.create(name='menu2', description='Test description', user=self.user2)
        dish_for_1 = Dish.objects.create(name='dish for menu1', description='Test description', price=10,
                            prepare_time=datetime.timedelta(days=0, seconds=800), menu=menu1)
        Dish.objects.create(name='dish for menu2', description='description', price=100,
                            prepare_time=datetime.timedelta(days=0, seconds=800), menu=menu2)

        response = self.client.get('/unpublic/dish/')
        self.assertEqual(len(response.data), 1)

        response = self.client.get('/unpublic/dish/menu1/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'dish for menu1')

        response = self.client.get('/unpublic/dish/menup/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(f'/unpublic/dish/menu1/{dish_for_1.id + 12}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(f'/unpublic/dish/menu1/{dish_for_1.id}/')
        self.assertEqual(response.data['id'], dish_for_1.id)

    def test_unpublic_dish_delete_put(self):
        self.client.force_login(self.user)
        menu1 = Menu.objects.create(name='menu1', description='Test description', user=self.user)
        dish_for_1 = Dish.objects.create(name='dish for menu1', description='Test description', price=10,
                                         prepare_time=datetime.timedelta(days=0, seconds=800), menu=menu1)
        response = self.client.put(f'/unpublic/dish/menu1/{dish_for_1.id}/',
                                   data={'name': 'dish for menu1', 'description': 'Updated description', 'price': 15,
                                         'prepare_time': datetime.timedelta(days=0, seconds=800), 'menu': menu1})
        self.assertEqual(response.data['description'], 'Updated description')

        response = self.client.delete(f'/unpublic/dish/menu1/{dish_for_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(menu1.dish_set.count(), 0)

    def test_unpublic_dish_post(self):
        self.client.force_login(self.user)
        menu1 = Menu.objects.create(name='menu1', description='Test description', user=self.user)
        response = self.client.post(f'/unpublic/dish/',
                                   data={'name': 'dish for menu1', 'description': 'Test description',
                                         'price': 115, 'prepare_time': datetime.timedelta(days=0, seconds=800),
                                         'menu': menu1})
        self.assertEqual(response.data['price'], '115.00')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)