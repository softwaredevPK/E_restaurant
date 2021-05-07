# eMenu
Project for recruitment purposes.


## Admin credentials:
admin
admin


## Celery commands
celery -A E_restaurant worker -l info
celery -A E_restaurant beat -l info/debug
celery -A proj beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler




