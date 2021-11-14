import os
import environ
import sys
import dj_database_url
from django.core.management.utils import get_random_secret_key


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(
    DEBUG=(bool, False)
)

READ_DOT_ENV_FILE = env.bool('READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    environ.Env.read_env()
    env_var = os.environ

DEBUG = os.getenv("DEBUG", "False") == "True"

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1, localhost").split(",")
# ALLOWED_HOSTS = ['www.maisaminherkku.fi', 'maisaminherkku.fi']

# Application definition

INSTALLED_APPS = [
    'main',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    "allauth.socialaccount",
    'crispy_forms',
    'corsheaders',
    'rest_framework',
    'multiselectfield',
    'star_ratings',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webshop.urls'

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
                'django.template.context_processors.media',

            ],
            'libraries':{
                # make your file entry here.
                'filter_tags': 'main.templatetags.filter',
            }
        },
    },
]

WSGI_APPLICATION = 'webshop.wsgi.application'


ACCOUNT_FORMS = {
    "login": "main.forms.SelfLoginForm", # Notice modification to LOGIN form.
    "signup": "main.forms.SelfSignUpForm",
    "add_email": "allauth.account.forms.AddEmailForm",
    "change_password": "allauth.account.forms.ChangePasswordForm",
    "set_password": "allauth.account.forms.SetPasswordForm",
    "reset_password": "allauth.account.forms.ResetPasswordForm",
    "reset_password_from_key": "allauth.account.forms.ResetPasswordKeyForm",
    "disconnect": "allauth.socialaccount.forms.DisconnectForm",
}

# Database

if os.getenv("DEVELOPMENT_MODE", "False") == "True":
    DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env("DB_NAME"),
        	'USER':	env("DB_USER"),
        	'PASSWORD': env("DB_PASSWORD"),
        	'HOST': env('DB_HOST'),
        	'PORT': env('DB_PORT'),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }

# Password validation

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

LANGUAGE_CODE = 'fi'


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:44100"]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Authenticate the allauth backage for login and signup with db

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE=False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
EMAIL_REQUIRED = True
ACCOUNT_SESSION_REMEMBER = False

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# X_FRAME_OPTIONS = "DENY"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_PORT = os.getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL=os.getenv("DEFAULT_FROM_EMAIL")



# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'WARNING',
#     },
# }

# crispy-forms for (Login and SignUp forms)

CRISPY_TEMPLATE_PACK = 'bootstrap4'
