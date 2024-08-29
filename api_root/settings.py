from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%p2qegn%)sah^7k13(8ssh4qdgaivm=-s+zchn8d4-5om&70c@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'api_rest',
    'compressor',
    'axes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'axes.middleware.AxesMiddleware',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

SESSION_COOKIE_NAME = 'sessionid'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# SECURE_HSTS_SECONDS = 3600  # 1 hora
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# veerificar nesse krlh qual é o SO e o navegador para setar os cookies
# 

# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = 'Lax'
ROOT_URLCONF = 'api_root.urls'

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]


AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # Tempo de espera em horas após exceder o limite de falhas

# Outras configurações do django-axes
AXES_LOCK_OUT_AT_FAILURE = True
AXES_USE_USER_AGENT = True
AXES_ONLY_USER_FAILURES = True
AXES_RESET_ON_SUCCESS = True

# SECURE_BROWSER_XSS_FILTER = True #ajuda a evitar ataque xss
# SECURE_CONTENT_TYPE_NOSNIFF = True # impede que a porra do navegador interprete outro tipo de conteudo que nao seja o especificado 
# SECURE_SSL_REDIRECT = True #Redireciona toda requisição HTTP para HTTPS

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

WSGI_APPLICATION = 'api_root.wsgi.application'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',  # Nome do serviço 'redis' definido no docker-compose
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# settings.py
AUTH_USER_MODEL = 'api_rest.User'

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Diretório onde os arquivos estáticos são coletados
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
