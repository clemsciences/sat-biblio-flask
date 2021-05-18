"""

"""

from functools import wraps
import logging
from typing import Union, List, AnyStr

from flask import request, session, abort
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import FreshTokenRequired
from flask_login import logout_user
from sat_biblio_server.utils import json_result

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


def disconnect_user():
    if logout_user():
        if "email" in session:
            del session["email"]
        if "first_name" in session:
            del session["first_name"]
        if "family_name" in session:
            del session["family_name"]
        if "right" in session:
            del session["right"]
        if "token" in session:
            del session["token"]
    else:
        print("strange")


def validation_connexion_et_retour_defaut(pseudo: Union[List, AnyStr], for_request_method=None):
    if not for_request_method:
        for_request_method = ["GET"]

    def deco(methode):
        @wraps(methode)
        def fonction_modifiee(*args, **kwargs):
            if request.method not in for_request_method:
                return methode(*args, **kwargs)
            if type(pseudo) == str:
                try:
                    verify_jwt_in_request()
                except FreshTokenRequired:
                    disconnect_user()
                if pseudo in session:
                    return methode(*args, **kwargs)
                logging.log(logging.DEBUG, "not connected")
                return json_result(False, "Vous n'êtes pas connecté"), 401
            else:
                logging.log(logging.DEBUG, "not connected")
                return json_result(False, "Vous n'êtes pas conencté"), 401
        return fonction_modifiee
    return deco
