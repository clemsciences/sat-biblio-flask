

import os

from sat_biblio_server.config import PACKDIR
from sat_biblio_server.config.constants import *

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


with open(os.path.join(PACKDIR, "email_address"), "r") as f:
    email_address = f.read().strip()

with open(os.path.join(PACKDIR, "mail_password"), "r") as f:
    password = f.read().strip()

secret_key = "SECRET"
with open(os.path.join(PACKDIR, "secret_key"), "r") as f:
    secret_key = f.read().strip()


with open(os.path.join(PACKDIR, "jwt_secret_key"), "r") as f:
    jwt_secret_key = f.read().strip()


class Config:
    ENV = "development"
    DEBUG = True
    TESTING = False
    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.dirname(__file__), '../data-dev.sqlite3')
    BABEL_DEFAULT_LOCALE = "fr"
    BABEL_DEFAULT_TIMEZONE = "Europe/Paris"
    # SERVER_NAME = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    WTF_CSRF_CHECK_DEFAULT = False
    JWT_SECRET_KEY = jwt_secret_key

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEBUG = True
    MAIL_USERNAME = email_address
    MAIL_PASSWORD = password
    MAIL_DEFAULT_SENDER = email_address
    # MAIL_MAX_EMAILS
    # MAIL_SUPPRESS_SEND : default app.testing
    # MAIL_ASCII_ATTACHMENTS : default False

    LANGUAGES = {
        "en": "English",
        "fr": "Français",
        "de": "Deutsch"
    }

    PERMANENT_SESSION_LIFETIME = 60*60*24*7
    CORS_HEADERS = 'Content-Type'
    SESSION_TYPE = "filesystem"

