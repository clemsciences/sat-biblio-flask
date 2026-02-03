

import datetime
import os

from sat_biblio_server.config import PACKDIR
from sat_biblio_server.config.constants import *

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def get_secret(name, default=None):
    path = os.path.join(PACKDIR, name)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return os.environ.get(name.upper(), default)


email_address = get_secret("email_address", "")
password = get_secret("mail_password", "")
secret_key = get_secret("secret_key", "SECRET")
jwt_secret_key = get_secret("jwt_secret_key", "JWT_SECRET")


class Config:
    ENV = "production"
    DEBUG = False
    TESTING = False
    SECRET_KEY = secret_key

    UPLOAD_FOLDER = os.environ.get("UPLOAD_DIR") or "uploads"
    UPLOAD_CATALOGUE_FOLDER = "catalogues"
    ALLOWED_IMPORT_EXTENSIONS = {"csv", "xslx"}
    MAX_CONTENT_LENGTH = 64_000_000

    BABEL_DEFAULT_LOCALE = "fr"
    BABEL_DEFAULT_TIMEZONE = "Europe/Paris"

    SERVER_NAME = "api.satbiblio.clementbesnier.eu"
    VUE_SERVER_NAME = "bht.societearcheotouraine.fr"

    # region sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or \
                              f'sqlite:///{os.path.join(os.environ.get("DATA_DIR", "/var/www/satbiblio.clementbesnier.eu/server"), "data-prod.sqlite3")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # endregion

    # region authentication
    WTF_CSRF_CHECK_DEFAULT = False
    # Ensure cookies are accepted in cross-site context when using HTTPS
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SAMESITE = 'None'
    REMEMBER_COOKIE_SECURE = True

    JWT_SECRET_KEY = jwt_secret_key
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=4)
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'None'
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=15)
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
    JWT_REFRESH_CSRF_HEADER_NAME = "X-CSRF-TOKEN-REFRESH"
    # endregion

    # region email
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEBUG = False
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
    CORS_ORIGINS = "https://bht.societearcheotouraine.fr"
    CORS_RESOURCES = "/*"
    CORS_SEND_WILDCARD = True
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_VARY_HEADER = True
    # endregion
