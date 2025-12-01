from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", "dev")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []
MS_FORMS_URL = os.environ.get("MS_FORMS_URL", "")

INSTALLED_APPS = [
"django.contrib.admin",
"django.contrib.auth",
"django.contrib.contenttypes",
"django.contrib.sessions",
"django.contrib.messages",
"django.contrib.staticfiles",
# terceiros
"django.contrib.sites",
"allauth",
"allauth.account",
"allauth.socialaccount",
"django_otp",
"guardian",
# apps
"accounts",
"metrics",
"uploads",
"dashboards",
]



SITE_ID = 1
ANONYMOUS_USER_NAME = "anon"
AUTHENTICATION_BACKENDS = (
"django.contrib.auth.backends.ModelBackend",
"allauth.account.auth_backends.AuthenticationBackend",
"guardian.backends.ObjectPermissionBackend",
)


MIDDLEWARE = [
"django.middleware.security.SecurityMiddleware",
"django.contrib.sessions.middleware.SessionMiddleware",
"django.middleware.common.CommonMiddleware",
"django.middleware.csrf.CsrfViewMiddleware",
"django.contrib.auth.middleware.AuthenticationMiddleware",
"allauth.account.middleware.AccountMiddleware",
"django_otp.middleware.OTPMiddleware",
"django.contrib.messages.middleware.MessageMiddleware",
"django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "visibilidade.urls"
TEMPLATES = [
{
"BACKEND": "django.template.backends.django.DjangoTemplates",
"DIRS": [BASE_DIR / "templates"],
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


WSGI_APPLICATION = "visibilidade.wsgi.application"


# DB via DATABASE_URL
import dj_database_url
DATABASES = {
"default": dj_database_url.parse(os.getenv("DATABASE_URL", "sqlite:///db.sqlite3"), conn_max_age=600)
}


# settings.py
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 3},
    },
]

# settings.py
ACCOUNT_PASSWORD_MIN_LENGTH = 3


LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Fortaleza"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/accounts/login/"
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = "/dashboard/me/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login/"
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = True          # ou False, se quiser só e-mail
# ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# NOVO (allauth 65+):
ACCOUNT_LOGIN_METHODS = {"username", "email"}  # ou {"email"} se preferir
ACCOUNT_SIGNUP_FIELDS = ["username*", "email*", "password1*", "password2*"]