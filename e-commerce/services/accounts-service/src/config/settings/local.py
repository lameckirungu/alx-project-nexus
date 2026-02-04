from .base import *  # noqa
DEBUG = True

import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "ecommerce"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "OPTIONS": {
            "options": f"-c search_path{os.getenv('DB_SCHEMA', 'public')}"
        },
    }
}