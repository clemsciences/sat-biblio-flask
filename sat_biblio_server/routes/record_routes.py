"""
Manages records in library.

Records are hints fto manage books in the library.
"""

import logging
import re

from flask import redirect, request

from routes import get_pagination, int_to_bool
from sat_biblio_server import sat_biblio
from sat_biblio_server.data.models import Enregistrement, ReferenceBibliographiqueLivre, Author
import sat_biblio_server.data.validation as dv
from sat_biblio_server.database import db, ReferenceBibliographiqueLivreDB, \
    EnregistrementDB
from sat_biblio_server.routes import validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region enregistrement
@sat_biblio.route("/book-records/", methods=["GET", "POST"])
@validation_connexion_et_retour_defaut("email", ["POST", "PUT"])
def book_records():
    if request.method == "POST":
        data = request.get_json()
        if dv.check_enregistrement(data):
            enregistrement_db = Enregistrement.from_data_to_db(data)
            db.session.add(enregistrement_db)
            db.session.commit()
            return json_result(True, id=enregistrement_db.id, message="L'enregistrement a correctement été sauvegardé."), 201
        return json_result(False, message="Erreur de la sauvegarde de l'enregistrement."), 400
    elif request.method == "GET":
        n_page, size, sort_by = get_pagination(request)

        # region filtre
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
        valid = request.args.get("valid", "1")
        if valid in ["1", "0"]:
            the_query = the_query.filter(EnregistrementDB.valide == int_to_bool(valid))
        else:
            the_query = the_query.filter(EnregistrementDB.valide == True)
        # endregion

        if sort_by:
            the_query = the_query.order_by(sort_by)

        enregistrements = []
        for record_db in the_query.paginate(page=n_page, per_page=size).items:
            record = Enregistrement.from_db_to_data(record_db)
            # print(record)
            if record and record['reference']:
                record["reference"] = record['reference']['titre']
                enregistrements.append(record)
            else:
                logging.error(f"record id = {record_db.id} record found "
                              f"but no bound reference")
        return json_result(True, enregistrements=enregistrements), 200


@sat_biblio.route("/book-records/<int:id_>/", methods=["GET", "DELETE", "PUT"])
@validation_connexion_et_retour_defaut("email", ["DELETE", "PUT"])
def book_record(id_):
    if request.method == "GET":
        # TODO valide?
        enregistrement_db = EnregistrementDB.query.filter_by(id=id_).first()
        if enregistrement_db:
            logging.warning(ReferenceBibliographiqueLivre.get_references_by_record(id_, 1, 10, ""))
            # logging.warning(Author.get_authors_by_record(id_, 1, 10, ""))
            enregistrement = Enregistrement.from_db_to_data(enregistrement_db)
            enregistrement["reference"] = {"text": enregistrement_db.reference.titre,
                                           "value": enregistrement_db.id_reference}
            return json_result(True, enregistrement=enregistrement), 200
        return json_result(False), 404
    elif request.method == "DELETE":
        enregistrement_db = EnregistrementDB.query.filter_by(id=id_).first()
        if enregistrement_db:
            db.session.delete(enregistrement_db)
            db.session.commit()
            return json_result(True), 204
        else:
            return json_result(False), 404
    elif request.method == "PUT":
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
            return json_result(True), 200
        return json_result(False), 404


@sat_biblio.route("/book-records/count/", methods=["GET"])
def book_records_count():
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

    valid = request.args.get("valid", "1")
    if valid in ["1", "0"]:
        the_query = the_query.filter(ReferenceBibliographiqueLivreDB.valide == int_to_bool(valid))
    else:
        the_query = the_query.filter(ReferenceBibliographiqueLivreDB.valide == True)

    number = the_query.count()
    logging.debug(number)
    return json_result(True, total=number), 200


@sat_biblio.route("/book-records/search/", methods=["POST"])
def chercher_enregistrements():
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
        return json_result(True, results=results), 200
    else:
        return json_result(True, results=[]), 200


@sat_biblio.route("/book-records/search-near/", methods=["GET"])
def chercher_enregistrements_proches():
    query_result = request.args.get("record")
    res = []
    if re.match(r"^(A|B|C|D|MM|BBH|GHA|GHB|GHC|GHbr|BBC|CAF|JSFA|RCAF|Congrès|"
                r"RCNSS|CNSS|CSS|TAB|FAG|FAM|FAP|MML|NUM|NUMbr) [0-9]{1,5}.*", query_result):

        book_records_db = EnregistrementDB.query.filter(EnregistrementDB.cote.like(f"%{query_result}%")).all()

        for book_record_db in book_records_db:
            if book_record_db:
                res.append(dict(text=f"{book_record_db.reference.titre} {book_record_db.cote}",
                                value=book_record_db.id))
    else:
        book_records_db = db.session\
            .query(EnregistrementDB, ReferenceBibliographiqueLivreDB)\
            .filter(EnregistrementDB.id_reference == ReferenceBibliographiqueLivreDB.id)\
            .filter(ReferenceBibliographiqueLivreDB.titre.like(f"%{query_result}%"))
        for book_record_db, ref_biblio_db in book_records_db:
            res.append(dict(text=f"{book_record_db.reference.titre} {book_record_db.cote}",
                            value=book_record_db.id))

    return json_result(True, suggestedRecords=res), 200
# endregion


# region entries
@sat_biblio.route("/book-records/<int:id_>/entries/", methods=["GET"])
def get_record_entries(id_):
    n_page, size, sort_by = get_pagination(request)
    entries = []
    authors = Author.get_authors_by_record(id_, n_page, size, sort_by)
    references = ReferenceBibliographiqueLivre.get_references_by_record(id_, n_page, size, sort_by)
    entries.extend(authors)
    entries.extend(references)
    return json_result(True, entries=entries), 200


@sat_biblio.route("/book-records/<int:id_>/entries/count/", methods=["GET"])
def get_record_count_entries(id_):
    author_count = Author.get_authors_by_record_count(id_)
    reference_count = ReferenceBibliographiqueLivre.get_references_by_record_count(id_)
    total = author_count + reference_count
    return json_result(True, total=total), 200
# endregion
