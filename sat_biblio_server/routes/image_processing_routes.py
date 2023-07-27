"""


"""


from flask import redirect, request, send_file
from skimage import *
from sat_biblio_server import sat_biblio, LogEventDB, UserDB
from sat_biblio_server.data.models import LogEvent
import sat_biblio_server.data.validation as dv
from sat_biblio_server.database import db
from sat_biblio_server.routes import get_pagination, int_to_bool, validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


@sat_biblio.route("/image-processing/")
def process_images():
    filename = ""
    return send_file(filename)
