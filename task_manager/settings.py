"""
Settings for the task_manager project.

All settings: https://docs.djangoproject.com/en/6.1/ref/settings/
"""

from pathlib import Path

# Root folder of the project. Use it like: BASE_DIR / "some_folder"
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Development only: change these before going to production ---

# Secret key is used for security (sessions, passwords). Keep it private.
SECRET_KEY = "django-insecure-a36ibj5w-vb1w%089f6m2qe0y&l41q@*7!kq==cq5n25_*8^*+"

# DEBUG=True shows detailed error pages. Turn it off in production.
DEBUG = True

ALLOWED_HOSTS = []

# --- Apps ---

# Every app must be listed here so Django can find its models, admin, etc.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    # Our own apps
    "tasks",
]

# Middleware runs on every request and response, from top to bottom
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# The main URL file that Django reads first
ROOT_URLCONF = "task_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "task_manager.wsgi.application"

# --- Database (PostgreSQL) ---

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "tasks",
        "USER": "postgres",
        "HOST": "localhost",
        "PASSWORD": "password",
        "PORT": 5432,
    }
}

# --- Password rules for users ---

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# --- Language and time zone ---

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True  # store dates in the database in UTC

# --- Static files (CSS, JavaScript, images) ---

STATIC_URL = "static/"

# --- Email: the console backend prints emails in the terminal ---

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}
