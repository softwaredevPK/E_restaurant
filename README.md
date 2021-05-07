# eMenu
Project for recruitment purposes.


## Admin credentials:
admin
admin


## Celery commands
celery -A eMenu worker -l info
celery -A eMenu beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

##coverage
coverage run manage.py test
coverage report -m

