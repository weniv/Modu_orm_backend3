```python
python -m venv venv
.\venv\Scripts\activate
pip install django
django-admin startproject config .
python manage.py migrate
python manage.py startapp main
python manage.py startapp blog

# config/settings.py
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    '...',
    'main',
    'blog',
]

"DIRS": [BASE_DIR / "templates"],

STATIC_URL = "static/"
STATIC_DIRS = [BASE_DIR / "static"]

# config/urls.py
