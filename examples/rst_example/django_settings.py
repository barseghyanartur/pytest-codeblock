# from pathlib import Path

# from django import conf, http, urls
# from django.core.handlers import asgi

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
# ]

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "django_db.sqlite3",
#     }
# }

# conf.settings.configure(
#     ALLOWED_HOSTS="*",
#     ROOT_URLCONF=__name__,
#     INSTALLED_APPS=INSTALLED_APPS,
#     DATABASES=DATABASES,
# )

# app = asgi.ASGIHandler()


# async def root(_request: http.HttpRequest) -> http.JsonResponse:
#     return http.JsonResponse({"message": "OK"})


# urlpatterns = [urls.path("", root)]

# ------
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "django_db.sqlite3",
    }
}

ROOT_URLCONF = "django_settings"

urlpatterns: list = []
