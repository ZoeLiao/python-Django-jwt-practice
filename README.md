# python-Django-jwt-practice

## Initialize
- `django-admin startproject <project_name>`
- `cd <project_name>`
- `django-admin startapp <app_name>`
- `python manage.py migrate`
- `python manage.py createsuperuser --email <your_email> --username <user_name>`

## Set Up
- `git clone [https://github.com/ZoeLiao/python-Django-jwt-practice.git](https://github.com/ZoeLiao/python-Django-jwt-practice.git)`
- `pyenv -m venv venv`
- `pip install -r requirements.txt`
- `cd src`
- `python manage.py runserver`

## URL
### Login
- URL: [http://127.0.0.1:8000/api/login](http://127.0.0.1:8000/api/login)
- Method: POST
- Body: {"phone": "0912345678", "password": "test"}

### Test API
- URL: [http://127.0.0.1:8000/api/test_api](http://127.0.0.1:8000/api/test_api)
- Method: GET
- Headers: {"Authorization": "Token <jwt_token>"}
- Response: {"msg": "Log in with jwt successfully."}

### Logout
- URL: [http://127.0.0.1:8000/api/logout](http://127.0.0.1:8000/api/logout)
- Method: GET
- Response: {"msg": "Log out successfully."}
