While (venv):
> pip install -r requirements

Make migrations:
> python simple_site/manage.py makemigrations
> python simple_site/manage.py migrate

Run the server:
> python simple_site/manage.py runserver

Endpoints (pk = desired primary key):

- **/**
- **/logout/**
- **/schema/**
- **/schema/**
- **schemas//**
- **schemas/create/**
- **schemas/edit/<int:pk>/**
- **schemas/delete/<int:pk>/**
- **schemas/export/<pk>/**

heroku: https://datafaker-csv.herokuapp.com

IMPORTANT: as my heroku acc didn't have credentials, I cannot run Redis, so celery.delay() doesn't work.