from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    prepare_time = models.DurationField()
    vegetarian = models.BooleanField(default=False)
    post_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, to_field='name')  # when Menu is deleted all related dishes should be deleted as well

    def __str__(self):
        return self.name
