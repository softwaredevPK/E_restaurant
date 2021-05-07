from celery import shared_task
import datetime

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models import Count, Q

from .models import Dish


@shared_task
def send_newsletter_email():
    emails = [i[0] for i in User.objects.values_list('email') if i[0] != '']
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    modified_dishes = Dish.objects.filter(update_date__year=yesterday.year,
                                          update_date__month=yesterday.month,
                                          update_date__day=yesterday.day). \
        filter(~Q(post_date__year=yesterday.year),
               ~Q(post_date__month=yesterday.month),
               ~Q(post_date__day=yesterday.day)). \
        values_list('name')
    new_dishes = Dish.objects.filter(post_date__year=yesterday.year,
                                     post_date__month=yesterday.month,
                                     post_date__day=yesterday.day). \
        values_list('name')
    content = 'Hi there,\n\nCheck out our new dishes:\n'
    updated = False
    if len(new_dishes) > 0:
        for i in new_dishes:
            content += f'• {i[0]}\n'
        content += '\n\n Some of our dishes has been modified, check them out:'
        updated = True
    if len(modified_dishes) > 0:
        for i in modified_dishes:
            content += f'• {i[0]}\n'
        content += '\n\nBest,\neMenu team'
        updated = True

    if not updated:
        content = 'Hi there,\n\nThere are not any new dishes on eMenu :/ \n\nBest,\neMenu team'
    send_mail(subject='eMenu Newsletter', message=content, from_email='eMenu', recipient_list=emails)
    return None
