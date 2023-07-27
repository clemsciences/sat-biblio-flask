
import datetime
import os

from sat_biblio_server.config import PACKDIR
from sat_biblio_server.config.constants import *
from sat_biblio_server.utils import UserRight


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

    UPLOAD_FOLDER = "uploads"
    UPLOAD_CATALOGUES_FOLDER = "catalogues"
    ALLOWED_IMPORT_EXTENSIONS = {"csv", "xslx"}
    MAX_CONTENT_LENGTH = 64_000_000

    BABEL_DEFAULT_LOCALE = "fr"
    BABEL_DEFAULT_TIMEZONE = "Europe/Paris"
    # SERVER_NAME = ""

    # region sqlalchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.dirname(__file__), '../data-dev.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # endregion

    # region authentication
    USERS = [
        dict(email="reader@gmail.com", password="reader", confirmed=True, is_admin=False, right=UserRight.lecteur),
        dict(email="contributor@gmail.com", password="contributor", confirmed=True, is_admin=False, right=UserRight.contributeur),
        dict(email="editor@gmail.com", password="editor", confirmed=True, is_admin=False, right=UserRight.editeur),
        dict(email="manager@gmail.com", password="manager", confirmed=True, is_admin=False, right=UserRight.gestionnaire),
        dict(email="admin@gmail.com", password="admin", confirmed=True, is_admin=True, right=UserRight.administrateur),
    ]

    WTF_CSRF_CHECK_DEFAULT = False
    JWT_SECRET_KEY = jwt_secret_key
    JWT_TOKEN_LOCATION = ['headers', 'cookies', "json", "query_string"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=4)
    JWT_COOKIE_SECURE = False
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(hours=4)
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
    JWT_REFRESH_CSRF_HEADER_NAME = "X-CSRF-TOKEN-REFRESH"
    # endregion

    # region email
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
    # endregion

    LANGUAGES = {
        "en": "English",
        "fr": "Français",
        "de": "Deutsch"
    }

    # region cors
    CORS_ALLOW_HEADERS = "*"
    CORS_ALWAYS_SEND = True
    CORS_AUTOMATIC_OPTIONS = True
    CORS_EXPOSE_HEADERS = ["Content-Type"]
    CORS_INTERCEPT_EXCEPTIONS = True
    CORS_MAX_AGE = None
    CORS_METHODS = ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"]
    CORS_ORIGINS = "http://localhost:8080"
    CORS_RESOURCES = "/*"
    CORS_SEND_WILDCARD = True
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_VARY_HEADER = True
    # endregion
