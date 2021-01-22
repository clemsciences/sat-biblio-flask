"""
Manages records in library.

Records are hints fto manage books in the library.
"""

import logging

from flask import redirect, request

from sat_biblio_server.data.models import Enregistrement
import sat_biblio_server.data.validation as dv
from sat_biblio_server.database import db, ReferenceBibliographiqueLivreDB, \
    EnregistrementDB
from sat_biblio_server.routes import sat_biblio, validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region enregistrement
@sat_biblio.route("/api/enregistrement/creer", methods=["POST"])
# @validation_connexion_et_retour_defaut("email", redirect("/api"))
def creer_enregistrement():
    data = request.get_json()
    if dv.check_enregistrement(data):
        enregistrement_db = Enregistrement.from_data_to_db(data)
        db.session.add(enregistrement_db)
        db.session.commit()
        return json_result(True, message="L'enregistrement a correctement été sauvegardé.")
    return json_result(False, message="Erreur de la sauvegarde de l'enregistrement.")


@sat_biblio.route("/api/enregistrement/lire/<int:id_>", methods=["GET"])
def lire_enregistrement(id_):
    enregistrement_db = EnregistrementDB.query.filter_by(id=id_).first()
    if enregistrement_db:
        enregistrement = Enregistrement.from_db_to_data(enregistrement_db)
        enregistrement["reference"] = {"text": enregistrement_db.reference.titre,
                                       "value": enregistrement_db.id_reference}
        return json_result(True, enregistrement=enregistrement)
    return json_result(False)


@sat_biblio.route("/api/enregistrement/supprimer/<int:id_>", methods=["GET"])
@validation_connexion_et_retour_defaut("email", redirect("/api"))
def supprimer_enregistrement(id_):
    enregistrement_db = EnregistrementDB.query.filter_by(id=id_).first()
    db.session.delete(enregistrement_db)
    db.session.commit()
    return json_result(True)


@sat_biblio.route("/api/enregistrement/modifier/<int:id_>", methods=["POST"])
@validation_connexion_et_retour_defaut("email", redirect("/api"))
def modifier_enregistrement(id_):
    data = request.get_json()
    enregistrement_db = EnregistrementDB.query.filter_by(id=id_).first()
    if enregistrement_db:
        if "id_reference" in data:
            enregistrement_db.id_reference = data["id_reference"]
        if "description" in data:
            enregistrement_db.description = data["description"]
        if "cote" in data:
            enregistrement_db.cote = data["cote"]
        if "annnee" in data:
            enregistrement_db.annee = data["annee"]
        if "nb_exemplaire_supp" in data:
            enregistrement_db.nb_exemplaire_supp = data["nb_exemplaire_supp"]
        if "provenance" in data:
            enregistrement_db.provenance = data["provenance"]
        if "mots_clef" in data:
            enregistrement_db.mots_clef = data["mots_clef"]
        db.session.commit()
        return json_result(True)
    return json_result(False)


@sat_biblio.route("/api/enregistrement/liste", methods=["GET"])
def liste_enregistrement():
    n_page = int(request.args.get("page"))
    size = int(request.args.get("size"))
    sort_by = request.args.get("sortBy")

    # region filtre
    cote = request.args.get("cote", "")
    titre = request.args.get("titre", "")
    mot_clef = request.args.get("mot_clef", "")

    the_query = EnregistrementDB.query
    if cote:
        the_query = the_query.filter(EnregistrementDB.cote.like(f"%{cote}%"))
    if titre:
        the_query = the_query.join(ReferenceBibliographiqueLivreDB)\
            .filter(ReferenceBibliographiqueLivreDB.titre.like(f"%{titre}%"))
    if mot_clef:
        the_query = the_query.filter(EnregistrementDB.mots_clef.like(f"%{mot_clef}%"))
    # endregion

    enregistrements = []
    for record_db in the_query.order_by(sort_by).paginate(page=n_page, per_page=size).items:
        record = Enregistrement.from_db_to_data(record_db)
        # print(record)
        record["reference"] = record['reference']['titre']
        enregistrements.append(record)
    return json_result(True, enregistrements=enregistrements)


@sat_biblio.route("/api/enregistrement/nombre", methods=["GET"])
def get_record_total_number():
    cote = request.args.get("cote", "")
    titre = request.args.get("titre", "")
    mot_clef = request.args.get("mot_clef", "")

    the_query = EnregistrementDB.query
    if cote:
        the_query = the_query.filter(EnregistrementDB.cote.like(f"%{cote}%"))
    if titre:
        the_query = the_query.join(ReferenceBibliographiqueLivreDB) \
            .filter(ReferenceBibliographiqueLivreDB.titre.like(f"%{titre}%"))
    if mot_clef:
        the_query = the_query.filter(EnregistrementDB.mots_clef.like(f"%{mot_clef}%"))
    number = the_query.count()
    logging.debug(number)
    return json_result(True, number=number)


@sat_biblio.route("/api/enregistrement/chercher", methods=["POST"])
def chercher_enregistrement():

    data = request.get_json()
    the_query = EnregistrementDB.query
    filtered = False
    if "description" in data and data["description"]:
        the_query.filter_by(description=data["description"])
        filtered = True
    if "cote" in data and data["cote"]:
        the_query.filter_by(cote=data["cote"])
        filtered = True
    if "annee" in data and data["annee"]:
        the_query.filter_by(annee=data["annee"])
        filtered = True
    if "provenance" in data and data["provenance"]:
        the_query.filter_by(provenance=data["provenance"])
        filtered = True
    if "mots_clef" in data and data["mots_clef"]:
        the_query.filter_by(mots_clef=data["mots_clef"])
        filtered = True
    if "valide" in data and data["valide"]:
        the_query.filter_by(valide=data["valide"])
        filtered = True
    if filtered:
        results_db = the_query.all()
        results = [Enregistrement.from_db_to_data(res) for res in results_db]
        return json_result(True, results=results)
    else:
        return json_result(True, results=[])
# endregion
