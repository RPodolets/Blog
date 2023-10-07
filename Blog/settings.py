import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "") != "False"


ALLOWED_HOSTS = [
    "bloggy-7uor.onrender.com",
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "core",
    "ckeditor",
    "ckeditor_uploader",
    "crispy_forms",
    "crispy_bootstrap5",
    "taggit",
    "storages",
]

AWS_ACCESS_KEY_ID = "AKIARSYAFXWSOE5WX5WC"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "bloggy-bucket"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_DEFAULT_ACL = "public-read"

TAGGIT_CASE_INSENSITIVE = True

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = "Blog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"]
        ,
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

WSGI_APPLICATION = "Blog.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = "staticfiles/"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

MEDIA_ROOT = ""

LOGIN_REDIRECT_URL = "/"

CKEDITOR_UPLOAD_PATH = "uploads/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar_Basic": [
            ["Source", "-", "Bold", "Italic"]
        ],
        "toolbar_YourCustomToolbarConfig": [
            {"name": "document", "items": ["Source", "-", "Save", "NewPage", "Preview", "Print", "-", "Templates"]},
            {"name": "clipboard", "items": ["Cut", "Copy", "Paste", "PasteText", "PasteFromWord", "-", "Undo", "Redo"]},
            {"name": "editing", "items": ["Find", "Replace", "-", "SelectAll"]},
            {"name": "forms",
             "items": ["Form", "Checkbox", "Radio", "TextField", "Textarea", "Select", "Button", "ImageButton",
                       "HiddenField"]},
            "/",
            {"name": "basicstyles",
             "items": ["Bold", "Italic", "Underline", "Strike", "Subscript", "Superscript", "-", "RemoveFormat"]},
            {"name": "paragraph",
             "items": ["NumberedList", "BulletedList", "-", "Outdent", "Indent", "-", "Blockquote", "CreateDiv", "-",
                       "JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock", "-", "BidiLtr", "BidiRtl",
                       "Language"]},
            {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
            {"name": "insert",
             "items": ["Image", "Flash", "Table", "HorizontalRule", "Smiley", "SpecialChar", "PageBreak", "Iframe"]},
            "/",
            {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]},
            {"name": "colors", "items": ["TextColor", "BGColor"]},
            {"name": "tools", "items": ["Maximize", "ShowBlocks"]},
            {"name": "about", "items": ["About"]},
            "/",  # put this to force next toolbar on new line
            {"name": "yourcustomtools", "items": [
                # put the name of your editor.ui.addButton here
                "Preview",
                "Maximize",

            ]},
        ],
        "toolbar": "YourCustomToolbarConfig",  # put selected toolbar config here
        # "toolbarGroups": [{ "name": "document", "groups": [ "mode", "document", "doctools" ] }],
        # "height": 291,
        # "width": "100%",
        # "filebrowserWindowHeight": 725,
        # "filebrowserWindowWidth": 940,
        # "toolbarCanCollapse": True,
        # "mathJaxLib": "//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML",
        "tabSpaces": 4,
        "extraPlugins": ",".join([
            "uploadimage",  # the upload image feature
            # your extra plugins here
            "div",
            "autolink",
            "autoembed",
            "embedsemantic",
            "autogrow",
            # "devtools",
            "widget",
            "lineutils",
            "clipboard",
            "dialog",
            "dialogui",
            "elementspath"
        ]),
    }
}
