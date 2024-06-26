import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'metrics',
    'courses',
    'event_logs',
    'corsheaders',
    'rest_framework',
    'users.apps.UsersConfig'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# TODO: REMOVE IT
CORS_ALLOW_ALL_ORIGINS = True  # For development only

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('REPORTS_DB_DATABASE', ''),
        'USER': os.environ.get('REPORTS_DB_USER', ''),
        'PASSWORD': os.environ.get('REPORTS_DB_PASSWORD', ''),
        'HOST': os.environ.get('REPORTS_DB_HOST', 'localhost'),
        'PORT': os.environ.get('REPORTS_DB_PORT'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

SIMPLE_JWT = {
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'UPDATE_LAST_LOGIN': True
}

# celery
CELERY_BROKER_URL = os.environ.get("REDIS_URL", "localhost")

CELERY_TASK_ROUTES = {
    "metrics.logic.celery_tasks.generate_report": {
        "queue": "sections"
    },
    "event_logs.tasks.unzip_logs_archive_task": {
        "queue": "logs"
    },
    "event_logs.tasks.decompress_zst": {
        "queue": "logs"
    },
    "event_logs.tasks.upload_logs": {
        "queue": "logs"
    }
}

# Redis
DEFAULT_REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', default='http://localhost:8080').split(" ")

MEDIA_URL = '/media/'
MEDIA_ROOT = '/media/'

ZIP_LOG_ARCHIVES_FOLDER = 'private/log_files/archives'
# Adding MEDIA_ROOT here is required because `zipfile` is not aware about Django media root folder
ZST_LOGS_FOLDER = str(os.path.join(MEDIA_ROOT, 'private/log_files/zst'))
PURE_LOGS_FOLDER = str(os.path.join(MEDIA_ROOT, 'private/log_files/logs'))

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 100