"""
Django settings for bellastores project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5pbvggw=#$4n-!+^1d3ca#g3#tc0tcokpjz$b!$bas*6)p&q7-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

# 11. Register the category app here and go to the models.py file of the category app to create your model
# 20. register the accounts app then go to the (accounts app) models.py file and create the account model.
# 33. Register the store app then we go to the store app (model.py # 34 ) file to create the store model.
# 64. We will register the carts app then create a (urls.py # 65) file in the carts app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 156 djange messages already installed. Next we will goto the bottom of this settings.py file to tell django we will be using messages by adding the code.
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'catigory',
    'store',
    'carts',
    'orders' # 264 Here we will add the order app to the list of installed apps, then we will goto the models.py # 265 file of the orders app to create our models.
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

ROOT_URLCONF = 'bellastores.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 3. Register the template folder inside the DIRS list[] - go to urls.py
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 48 We will include our category context_processor so that we can be able to call/use the 
                # menu_link() method i.e category list(shirts, jeans), in any template we want. 
                # it will be available in all the template. i.e the navbar.html # 49
                'catigory.context_processors.menu_links',

                # 96 We will register the cart context_processor so we can call the cart_count variable in our 
                # template (i.e navbar.html # 97) and then we can see the total item in cart. 
                'carts.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'bellastores.wsgi.application'

# 24 this tells the settings that we are going to use custom user model. 
# where (accounts) is our app name and (.Account) is the model name
# Next we need to register the model(Account model) in the admin.py file of the accounts app as # 25
AUTH_USER_MODEL = 'accounts.Account' 

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# 5. HERE WE LINK THE STATIC FOLDER IN OUR BASE DIRECTORY(PROJECT APP-bellastore)
# 6. open the terminal window and run the command -(python manage.py collectstatic) to collect all static files in the static folder 
# 6. and create a new stitic file in the root folder(main folder) to be used for our website
# 6. you will see that a new static folder is crfeated and it also created a folder in the static folder called admin containing all items in the static folder
# 6. Next is to load the static files inside the html file(home.html) go to home.html
STATIC_ROOT = BASE_DIR /'static'
STATICFILES_DIRS = [
    'bellastores/static',
]
# end # 6
# 29 we will write the media file configuration here for upload of files(categories images) 
# then we will go to (url.py) # 30 of the project app to add(+) the static function to the urlpatterns
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR /'media'
# end 29

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 157 Here is the code to tell django we are using messages. Next we will create a file # 158 alert.html in our templates/includes folder
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    # messages.INFO: 'value',
    messages.ERROR: 'danger', # where INFO or ERROR is the name of the bootstrap class.
}

# 175 We will write/configure our smtp to send emails 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.securedglobalasset.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@securedglobalasset.com'
EMAIL_HOST_PASSWORD = 'globalasset100%'
EMAIL_USE_TLS = True
# 175 ends and SMTP configuration is completed. Next we goto the # 176 urls.py file of the accounts app to add the 'activate' url used in the account_verification_email.html file.
