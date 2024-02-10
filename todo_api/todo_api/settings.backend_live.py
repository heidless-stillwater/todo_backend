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
env_file = os.path.join(BASE_DIR, "config/.env")

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
# [START_EXCLUDE]
elif os.getenv("TRAMPOLINE_CI", None):
    # Create local settings if running with CI, for unit testing
    print("TRAMPOLINE_CI")
    placeholder = (
        f"SECRET_KEY=a\n"
        "GS_BUCKET_NAME=None\n"
        f"DATABASE_URL=sqlite://{os.path.join(BASE_DIR, 'db.sqlite3')}"
    )
    env.read_env(io.StringIO(placeholder))
# [END_EXCLUDE]
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    
    print(f"using secrets settings: {settings_name}")
    
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    
    
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
    
    print(f"SECRETS: {payload}")
    print(f"env settings: {env.read_env(io.StringIO(payload))}")

    env.read_env(io.StringIO(payload))
    print(f"SECRETS PAYLOAD: {env.read_env(io.StringIO(payload))}")
else:
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")
# [END cloudrun_django_secret_config]
SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

# [START cloudrun_django_csrf]
# SECURITY WARNING: It's recommended that you use this when
# running in production. The URL will be known once you first deploy
# to Cloud Run. This code takes the URL and converts it to both these settings formats.
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    print(f"CLOUDRUN_SERVICE_URL: {CLOUDRUN_SERVICE_URL}")
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
#    ALLOWED_HOSTS = CLOUDRUN_SERVICE_URL, 'localhost', '127.0.0.1'
    print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
#    TST = CLOUDRUN_SERVICE_URL, 'localhost'
#    print(TST)
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
    print(f"CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}")
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    ALLOWED_HOSTS = ["*"]

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
    "storages",
    
    # Local
    'about',
    'projects',
    'research',
    'technologies',
    'contact',
    'upload',
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

ROOT_URLCONF = "config.urls"

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
WSGI_APPLICATION = "config.wsgi.application"

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

# If the flag as been set, configure to use proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 1234

# [END cloudrun_django_database_config] #

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

# Static files (CSS, JavaScript, Images)
# [START cloudrun_django_static_config]
# Define static storage via django-storages[google]
from google.oauth2 import service_account
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, 'config/heidless-pfolio-deploy-2-7240e1b72d37.json')
)
#STATIC_URL = "/static/"
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"

STATIC_URL = 'https://storage.cloud.google.com/pfolio-backend-bucket-2/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# [END cloudrun_django_static_config]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
