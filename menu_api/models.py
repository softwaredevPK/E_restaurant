from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField()
    post_date = models.DateTimeField(auto_now_add=False)
    update_date = models.DateTimeField(auto_now=True)


class Dish(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    prepare_time = models.DurationField()
    vegetarian = models.BooleanField(default=False)
    post_date = models.DateTimeField(auto_now_add=False)
    update_date = models.DateTimeField(auto_now=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)  # when Menu is deleted all related dishes should be deleted as well
