"""

"""

from flask import url_for, flash, send_file, session, redirect, session, \
    jsonify, request, abort

import logging

from sqlalchemy import or_

from data.models import ReferenceBibliographiqueLivre, Author, Enregistrement
from sat_biblio_server.database import db, AuthorDB, ReferenceBibliographiqueLivreDB, \
    EnregistrementDB, EmpruntLivreDB, UserDB
from sat_biblio_server.managers import mail_manager
from sat_biblio_server import sat_biblio
from sat_biblio_server.routes import validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region export

# endregion

# region recherche
@sat_biblio.route("/api/rechercher", methods=["POST"])
def rechercher():
    # data = request.get_json()
    # print(data)
    # authors_db = AuthorDB.query.filter_by().all()
    # references_db = ReferenceBibliographiqueLivreDB.query.filter_by().all()
    # enregistrements_db = EnregistrementDB.query.filter_by().all()
    return json_result(True, resultats=[])
# endregion


