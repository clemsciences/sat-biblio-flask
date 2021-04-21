"""

"""

from functools import wraps
import logging
from typing import Union, List, AnyStr

from flask import request, session, abort

from sat_biblio_server import sat_biblio

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


def validation_connexion_et_retour_defaut(pseudo: Union[List, AnyStr], val, for_request_method=None):
    if not for_request_method:
        for_request_method = ["GET"]

    def deco(methode):
        @wraps(methode)
        def fonction_modifiee(*args, **kwargs):
            if request.method not in for_request_method:
                return methode(*args, **kwargs)
            if type(pseudo) == str:
                if pseudo in session:
                    return methode(*args, **kwargs)
                logging.log(logging.DEBUG, "not connected")
                return val, 401
            else:
                logging.log(logging.DEBUG, "not connected")
                return val, 401
        return fonction_modifiee
    return deco


@sat_biblio.route("/shutdown")
def server_shutdown():
    if not sat_biblio.Config.TESTING:
        abort(404)
    shutdown = request.environ.get("werkzeug.server.shutdown")
    if not shutdown:
        abort(500)
    shutdown()
    return "Shutting down"
