"""

"""

from functools import wraps
import logging
from typing import Union, List, AnyStr

from flask import request, session, abort
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_jwt_extended.exceptions import FreshTokenRequired
from flask_login import logout_user
from sat_biblio_server.utils import json_result, UserRight


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
                # Accept either a valid JWT or a valid session
                try:
                    verify_jwt_in_request()
                    return methode(*args, **kwargs)
                except FreshTokenRequired:
                    disconnect_user()
                    logging.log(logging.ERROR, "disconnected")
                except Exception:
                    # No valid JWT in the request, fall back to session check
                    pass
                if pseudo in session:
                    return methode(*args, **kwargs)
                logging.log(logging.ERROR, "not connected")
                return json_result(False, "Vous n'êtes pas connecté"), 401
            else:
                logging.log(logging.ERROR, "not connected")
                return json_result(False, "Vous n'êtes pas conencté"), 401
        return fonction_modifiee
    return deco


def validation_droit_et_retour_defaut(required_right: UserRight, for_request_method=None):
    """
    Enforces authorization (not just authentication).

    Checks, in order:
    - If a valid JWT is present: looks for a 'right' claim in JWT (e.g. 'administrateur')
    - Otherwise falls back to Flask session: session['right']

    Returns 403 if authenticated but not allowed.
    """
    if not for_request_method:
        for_request_method = ["POST", "PUT", "DELETE"]

    def deco(methode):
        @wraps(methode)
        def fonction_modifiee(*args, **kwargs):
            if request.method not in for_request_method:
                return methode(*args, **kwargs)

            # Prefer JWT if present/valid
            try:
                verify_jwt_in_request()
                claims = get_jwt() or {}
                jwt_right = claims.get("right")
                print(jwt_right, required_right.value)
                if jwt_right >= required_right.value:
                    return methode(*args, **kwargs)
                return json_result(False, message="Accès interdit."), 403
            except Exception:
                # No (valid) JWT -> fall back to session
                pass

            if session.get("right") == required_right:
                return methode(*args, **kwargs)

            return json_result(False, message="Accès interdit."), 403

        return fonction_modifiee
    return deco