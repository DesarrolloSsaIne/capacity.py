"""
Django settings for proyecto_django project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.urls import reverse_lazy


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o#&r)$g9u5)%9!%w1e6sgi^0yrj-ocbu24&)2*ldlox#(ysd^t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# LDAP auth settings.

AUTHENTICATION_BACKENDS = (
'django.contrib.auth.backends.ModelBackend',
'django_python3_ldap.auth.LDAPBackend',
)

LDAP_AUTH_URL = "ldap://zeus.ine.cl"
LDAP_AUTH_USE_TLS = False
LDAP_AUTH_SEARCH_BASE = "ou=INE,DC=ine,DC=cl"
LDAP_AUTH_OBJECT_CLASS = "organizationalPerson"

LDAP_AUTH_USER_FIELDS = {
"username": "sAMAccountName",
"first_name": "givenName",
"last_name": "sn",
"email": "mail",
}


LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)

#LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"

#LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"

#LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"

LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory"

LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "INE"
#
# LDAP_AUTH_CONNECTION_USERNAME = 'jrodriguez' #|| Si le da la chiripiorca al sincronizar descomentar
# LDAP_AUTH_CONNECTION_PASSWORD = 'JR14202112-9'  #|| Si le da la chiripiorca al sincronizar descomentar

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django_python3_ldap": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

# Application definition



INSTALLED_APPS = [


    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'django_python3_ldap',
    'sitetree',
    'mathfilters',




    'apps.eje',
    'apps.registration',

    'apps.periodos',

    'apps.estructura',
    'apps.objetivos',
    'apps.jefaturas',
    'apps.familia_cargo',
    'apps.gestion_horas',
    'apps.feriados',
    'apps.vista_objetivos',
    'apps.periodicidad',
    'apps.productos',
    'apps.estado_flujo',
    'apps.controlador',
    'apps.actividades',
    'apps.valida_plan',
    'apps.valida_plan2',
    'apps.perfiles',

    'apps.estado_actividad',
    'apps.estado_plan',
    'apps.estado_seguimiento',
    'apps.revision_planificacion',
    'apps.seguimiento_formula',
    'apps.reportes',
    'apps.planificacion_admin',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proyecto_django.urls'

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
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',



            ],
        },
    },
]

WSGI_APPLICATION = 'proyecto_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases



# DATABASES = {
#    'default': {
#        'ENGINE': 'mysql_cymysql',
#        'NAME': 'DJANGODB',
#        'USER': 'usuariocapacity',
#        'PASSWORD': 'FoXoWu',
#        'HOST': '10.91.160.53',
#        'PORT': 3306,
#    }
# }

DATABASES = {
    'default': {
        'ENGINE': 'mysql_cymysql',
        'NAME': 'django_local_uno_desa',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'mysql_cymysql',
#         'NAME': 'DJANGO_DES',
#         'USER': 'capacity_des',
#         'PASSWORD': '2MOMO99L',
#         'HOST': '10.91.160.53',
#         'PORT': 3306,
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'mysql_cymysql',
#         'NAME': 'CAPACITY_DB_PRDx',
#         'USER': 'jasonx',
#         'PASSWORD': '1SUMU79Sx',
#         'HOST': '10.91.163.94',
#         'PORT': 3306,
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]


#LOGIN_REDIRECT_URL = reverse_lazy('solicitud_lista')
#LOGOUT_REDIRECT_URL = reverse_lazy('logout')
#DATE_INPUT_FORMATS = ['%d-%m-%Y']

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'jasonrd2@gmail.com'
# EMAIL_HOST_PASSWORD = 'rodrigue0217'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DEFAULT_FROM_EMAIL = 'jasonrd2@gmail.com'

EMAIL_USE_TLS = False
EMAIL_HOST = '192.168.1.235'
EMAIL_PORT = 25
# EMAIL_HOST_USER = 'capacity.planificacion@ine.cl'
# EMAIL_HOST_PASSWORD = '(Morande_801)'
EMAIL_HOST_USER = 'jason.rodriguez@ine.cl'
EMAIL_HOST_PASSWORD = 'JR14202112-9'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = False



