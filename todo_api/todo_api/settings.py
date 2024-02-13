# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os
from urllib.parse import urlparse

import environ
import google.auth
from google.cloud import secretmanager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# [START cloudrun_django_secret_config]
# SECURITY WARNING: don't run with debug turned on in production!
# Change this to "False" when you are ready for production
env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, ".env")

#print("#####################")
#print(os.getenv('DATABASE_URL'))
#print(os.getenv('GS_BUCKET_NAME'))
#print(os.getenv('SECRET_KEY'))
#print(os.getenv('FRONTEND_URL'))

# print(os.getenv('DATABASE_NAME'))
# print(os.getenv('DATABASE_USER'))
# print(os.getenv('DATABASE_PASS'))
# print(os.getenv('DATABASE_HOST'))
# print(os.getenv('DATABASE_PORT'))
# print("#####################")

#         #'HOST': '35.189.112.171',
#         #'HOST': '10.154.0.3',   # insternal IP

# print(f'checking for {env_file}')



# Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
    print(f"DEFAULT GOOGLE PROJECT: {google.auth.default()}")
except google.auth.exceptions.DefaultCredentialsError:
    pass

print(f'checking for {env_file}')
if os.path.isfile(env_file):
    # Use a local secret file, if provided
    print("### Using local secret file")
    print('env-file: ' + env_file)
    env.read_env(env_file)
    
SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

# ALLOWED_HOSTS = [
#     "*",
#     "http://127.0.0.1"
# ]

print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# [END cloudrun_django_csrf]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    'rest_framework',
    'corsheaders',

    'todos',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:3001',
]

ROOT_URLCONF = 'todo_api.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = 'todo_api.wsgi.application'

# Database
# [START cloudrun_django_database_config]
# Use django-environ to parse the connection string

DATABASES = {"default": env.db()}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.getenv('DATABASE_NAME'),
#       'USER': os.getenv('DATABASE_USER'),
#        'PASSWORD': os.getenv('DATABASE_PASS'),
#        'HOST': os.getenv('DATABASE_HOST'),
###       #'HOST': '35.189.112.171',
###       #'HOST': '10.154.0.3',   # insternal IP
#        'PORT': os.getenv('DATABASE_PORT'),
##        'PORT': '', # leave blank so the default port is selected
#    }
#}


# # If the flag as been set, configure to use proxy
# if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
#     DATABASES["default"]["HOST"] = "127.0.0.1"
#     DATABASES["default"]["PORT"] = 1234
# # [END cloudrun_django_database_config] #

# Password validation

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


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
# STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
# GS_DEFAULT_ACL = "publicRead"

# STATIC_URL = 'https://storage.cloud.google.com/pfolio-todo-bucket-2/'
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# [END cloudrun_django_static_config]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
