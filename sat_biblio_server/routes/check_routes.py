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
            if type(pseudo) != str:
                logging.log(logging.ERROR, "not connected")
                return json_result(False, "Vous n'êtes pas connecté"), 401
            # Un JWT valide ou une session valide suffit. La vue est appelée
            # hors du try : une erreur dans la vue ne doit pas être prise pour
            # un défaut d'authentification (ni provoquer un second appel).
            connected = False
            try:
                verify_jwt_in_request()
                connected = True
            except FreshTokenRequired:
                disconnect_user()
                logging.log(logging.ERROR, "disconnected")
            except Exception:
                # Pas de JWT valide : on se rabat sur la session.
                pass
            if connected or pseudo in session:
                return methode(*args, **kwargs)
            logging.log(logging.ERROR, "not connected")
            return json_result(False, "Vous n'êtes pas connecté"), 401
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

            # Le JWT est prioritaire ; à défaut, on se rabat sur la session.
            # La vue est appelée hors du try : une erreur dans la vue ne doit
            # pas être transformée en 403 (ni provoquer un second appel).
            user_right = None
            try:
                verify_jwt_in_request()
                user_right = (get_jwt() or {}).get("right")
            except Exception:
                user_right = session.get("right")

            if isinstance(user_right, int) and user_right >= required_right.value:
                return methode(*args, **kwargs)
            return json_result(False, message="Accès interdit."), 403

        return fonction_modifiee
    return deco