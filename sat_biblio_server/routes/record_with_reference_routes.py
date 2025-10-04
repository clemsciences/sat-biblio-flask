"""
Manages records in the library.

Records are hints to manage books in the library.
"""
import json
import logging
import os
import re

from flask import request, session, send_file
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

import sat_biblio_server.data.validation as dv
from sat_biblio_server.managers.catalogue_manager import Catalogue2025, Catalogue2025Row
from sat_biblio_server.managers.export_manager import ExportCatalogueManager
from sat_biblio_server import sat_biblio, Author2023DB
from sat_biblio_server.data.models_2023 import Enregistrement2023, ReferenceBibliographiqueLivre2023, Author2023, \
    EnregistrementComplet2023
from sat_biblio_server.database import db, ReferenceBibliographiqueLivre2023DB, \
    Enregistrement2023DB
from sat_biblio_server.managers.log_manager import LogEventManager
from sat_biblio_server.routes import get_pagination, validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region enregistrement
@sat_biblio.route("/book-records-with-reference/", methods=["GET", "POST"])
@validation_connexion_et_retour_defaut("email", ["POST", "PUT"])
def book_records_with_reference():
    if request.method == "POST":
        data = request.get_json()
        if dv.check_enregistrement_complet(data):
            reference_db, enregistrement_db = EnregistrementComplet2023.from_data_to_db(data)

            db.session.add(reference_db)
            db.session.commit()

            enregistrement_db.id_reference = reference_db.id
            db.session.add(enregistrement_db)
            db.session.commit()

            LogEventManager(db).add_create_event(reference_db.id, session.get("id", -1),
                                                 ReferenceBibliographiqueLivre2023DB.__tablename__,
                                                 values = json.dumps(
                                                     ReferenceBibliographiqueLivre2023.from_db_to_data(reference_db)))
            LogEventManager(db).add_create_event(enregistrement_db.id, session.get("id", -1),
                                                 Enregistrement2023DB.__tablename__,
                                                 values=json.dumps(
                                                     Enregistrement2023.from_db_to_data(enregistrement_db)))
            return json_result(True, id=enregistrement_db.id,
                               message="L'enregistrement a correctement été sauvegardé."), 201
        return json_result(False, message="Erreur de la sauvegarde de l'enregistrement."), 400
    elif request.method == "GET":
        n_page, size, sort_by = get_pagination(request)

        # region filtre
        cote = request.args.get("cote", "")
        titre = request.args.get("titre", "")
        mot_clef = request.args.get("mot_clef", "")
        author = request.args.get("author", "")

        the_query = Enregistrement2023DB.query
        if cote:
            the_query = the_query.filter(Enregistrement2023DB.cote.ilike(f"%{cote}%"))
        if titre:
            the_query = the_query.join(ReferenceBibliographiqueLivre2023DB) \
                .filter(ReferenceBibliographiqueLivre2023DB.titre.ilike(f"%{titre}%"))
        if mot_clef:
            the_query = the_query.filter(Enregistrement2023DB.aide_a_la_recherche.like(f"%{mot_clef}%"))
        if author:
            the_query = (the_query
                         .join(ReferenceBibliographiqueLivre2023DB)
                         .join(ReferenceBibliographiqueLivre2023DB.authors)
                         .filter(or_(Author2023DB.first_name.ilike(f"%{author}%"),
                                     Author2023DB.family_name.ilike(f"%{author}%"))
                                 )
                         ).options(
                            joinedload(Enregistrement2023DB.reference)
                            .joinedload(ReferenceBibliographiqueLivre2023DB.authors)
                        )
        # endregion

        if sort_by:
            the_query = the_query.order_by(Enregistrement2023DB.cote)
        else:
            the_query = the_query.order_by(Enregistrement2023DB.cote)

        enregistrements = []
        for record_db in the_query.paginate(page=n_page, per_page=size).items:
            record = Enregistrement2023.from_db_to_data(record_db)
            # print(record)
            if record and record['reference']:
                record["authors"] = ", ".join([author["first_name"] + " " + author["family_name"] for author in record["reference"]['authors']])
                record["reference"] = record['reference']['titre']
                enregistrements.append(record)
            else:
                logging.error(f"record id = {record_db.id} record found "
                              f"but no bound reference")
        return json_result(True, enregistrements=enregistrements), 200

@sat_biblio.route("/book-records-with-reference/export/", methods=["GET"])
def book_records_with_reference_export():
    if request.method == "GET":
        # region filtre
        cote = request.args.get("cote", "")
        titre = request.args.get("titre", "")
        mot_clef = request.args.get("mot_clef", "")
        author = request.args.get("author", "")

        the_query = Enregistrement2023DB.query
        if cote:
            the_query = the_query.filter(Enregistrement2023DB.cote.ilike(f"%{cote}%"))
        if titre:
            the_query = the_query.join(ReferenceBibliographiqueLivre2023DB) \
                .filter(ReferenceBibliographiqueLivre2023DB.titre.ilike(f"%{titre}%"))
        if mot_clef:
            the_query = the_query.filter(Enregistrement2023DB.aide_a_la_recherche.like(f"%{mot_clef}%"))
        if author:
            the_query = (the_query
                         .join(ReferenceBibliographiqueLivre2023DB)
                         .join(ReferenceBibliographiqueLivre2023DB.authors)
                         .filter(or_(Author2023DB.first_name.ilike(f"%{author}%"),
                                     Author2023DB.family_name.ilike(f"%{author}%"))
                                 )
                         ).options(
                            joinedload(Enregistrement2023DB.reference)
                            .joinedload(ReferenceBibliographiqueLivre2023DB.authors)
                        )
        the_query = the_query.order_by(Enregistrement2023DB.cote)

        enregistrements = []
        for record_db in the_query.all():
            enregistrements.append(record_db)

        catalogue_to_export = Catalogue2025()
        catalogue_to_export.rows = [Catalogue2025Row(record_db) for record_db in enregistrements]
        complete_path = ExportCatalogueManager.export_2025(os.path.join(os.getcwd(), "export"), catalogue_to_export, "export-recherche-", "Export de la recherche", False)
        # return json_result(True, complete_path=complete_path), 200
        return send_file(complete_path)
    return json_result(False, message="Erreur lors de l'export."), 400


@sat_biblio.route("/book-records-with-reference/<int:id_>/", methods=["GET", "DELETE", "PUT"])
@validation_connexion_et_retour_defaut("email", ["DELETE", "PUT"])
def book_record_with_reference(id_):
    if request.method == "GET":
        # TODO valide?
        record = None
        reference = None
        enregistrement_complet = None
        previous_record_db = Enregistrement2023DB.query.filter_by(id=id_).first()
        if previous_record_db:
            logging.warning(ReferenceBibliographiqueLivre2023.get_references_by_record(id_, 1, 10, ""))
            # logging.warning(Author.get_authors_by_record(id_, 1, 10, ""))
            record = Enregistrement2023.from_db_to_data(previous_record_db)
            reference_db = ReferenceBibliographiqueLivre2023DB.query.filter_by(id=previous_record_db.reference.id).first()
            if reference_db:
                enregistrement_complet = EnregistrementComplet2023.from_db_to_data(reference_db, previous_record_db)
                # enregistrement["reference"] = ReferenceBibliographiqueLivre2023.from_db_to_data(reference_db)
                # enregistrement["reference"]["text"] = enregistrement_db.reference.titre
                # enregistrement["reference"]["value"] = enregistrement_db.id_reference
                reference = ReferenceBibliographiqueLivre2023.from_db_to_data(reference_db)
                authors = [
                    dict(text=f"{author_db.first_name} {author_db.family_name}", value=author_db.id,
                         family_name=author_db.family_name, first_name=author_db.first_name)
                    for author_db in reference_db.authors]
                reference["authors"] = authors
                enregistrement_complet["authors"] = authors
                return json_result(True,
                                   record=record,
                                   reference=reference,
                                   record_with_reference=enregistrement_complet), 200
        return json_result(False), 404
    elif request.method == "DELETE":
        previous_record_db = Enregistrement2023DB.query.filter_by(id=id_).first()
        if previous_record_db:
            record_data = Enregistrement2023.from_db_to_data(previous_record_db)
            db.session.delete(previous_record_db)
            db.session.commit()
            LogEventManager(db).add_delete_event(previous_record_db.id, session.get("id", -1),
                                                 Enregistrement2023DB.__tablename__,
                                                 values=json.dumps(record_data))  # TODO
            return json_result(True), 204
        else:
            return json_result(False), 404
    elif request.method == "PUT":
        data = request.get_json()

        if dv.check_enregistrement_complet(data):
            previous_record_db = Enregistrement2023DB.query.filter_by(id=id_).first()
            previous_reference_db = (ReferenceBibliographiqueLivre2023DB
                                     .query
                                     .filter_by(id=previous_record_db.id_reference)
                                     .first())
            previous_reference_data = ReferenceBibliographiqueLivre2023.from_db_to_data(previous_reference_db)
            previous_record_data = Enregistrement2023.from_db_to_data(previous_record_db)
            current_reference_db, current_record_db = EnregistrementComplet2023.from_data_to_db(data)

            previous_record_db.observations = current_record_db.observations
            previous_record_db.cote = current_record_db.cote
            previous_record_db.annee_obtention = current_record_db.annee_obtention
            # previous_record_db.nb_exemplaire_supp = current_record_db.nb_exemplaire_supp
            previous_record_db.provenance = current_record_db.provenance
            previous_record_db.aide_a_la_recherche = current_record_db.aide_a_la_recherche

            previous_reference_db.authors = current_reference_db.authors
            previous_reference_db.authors_form = current_reference_db.authors_form
            previous_reference_db.titre = current_reference_db.titre
            previous_reference_db.editeur = current_reference_db.editeur
            previous_reference_db.lieu_edition = current_reference_db.lieu_edition
            previous_reference_db.annee = current_reference_db.annee
            previous_reference_db.nb_page = current_reference_db.nb_page
            previous_reference_db.date_derniere_modification = current_reference_db.date_derniere_modification
            previous_reference_db.description = current_reference_db.description

            previous_record_db.reference = previous_reference_db


            # if "id_reference" in data:
            #     previous_record_db.id_reference = data["id_reference"]
            # if "description" in data:
            #     previous_record_db.description = data["description"]
            # if "cote" in data:
            #     previous_record_db.cote = data["cote"]
            # if "annnee" in data:
            #     previous_record_db.annee = data["annee"]
            # if "nb_exemplaire_supp" in data:
            #     previous_record_db.nb_exemplaire_supp = data["nb_exemplaire_supp"]
            # if "provenance" in data:
            #     previous_record_db.provenance = data["provenance"]
            # if "aide_a_la_recherche" in data:
            #     previous_record_db.aide_a_la_recherche = data["aide_a_la_recherche"]
            #
            # previous_record_db.
            db.session.commit()



            LogEventManager(db).add_update_event(id_,
                                                 session.get("id", -1),
                                                 ReferenceBibliographiqueLivre2023DB.__tablename__,
                                                 values=json.dumps(dict(previous=previous_reference_data,
                                                                        new=ReferenceBibliographiqueLivre2023.from_db_to_data(current_reference_db))))
            LogEventManager(db).add_update_event(id_,
                                                 session.get("id", -1),
                                                 Enregistrement2023DB.__tablename__,
                                                 values=json.dumps(dict(previous=previous_record_data,
                                                                        new=Enregistrement2023.from_db_to_data(current_record_db))))
            return json_result(True, "Enregistrement correctement mis à jour."), 200
        return json_result(False, "Echec de la mis à jour de l'enregistrement."), 500
    return json_result(False, "Echec de la requête."), 404


@sat_biblio.route("/book-records-with-reference/count/", methods=["GET"])
def book_records_with_reference_count():
    cote = request.args.get("cote", "")
    titre = request.args.get("titre", "")
    mot_clef = request.args.get("mot_clef", "")
    author = request.args.get("author", "")

    the_filtered_query = Enregistrement2023DB.query
    the_total_query = Enregistrement2023DB.query
    if cote:
        the_filtered_query = the_filtered_query.filter(Enregistrement2023DB.cote.ilike(f"%{cote}%"))
    if titre:
        the_filtered_query = the_filtered_query.join(ReferenceBibliographiqueLivre2023DB) \
            .filter(ReferenceBibliographiqueLivre2023DB.titre.ilike(f"%{titre}%"))
    if mot_clef:
        the_filtered_query = the_filtered_query.filter(Enregistrement2023DB.aide_a_la_recherche.ilike(f"%{mot_clef}%"))
    if author:
        the_filtered_query = (the_filtered_query
                     .join(ReferenceBibliographiqueLivre2023DB)
                     .join(ReferenceBibliographiqueLivre2023DB.authors)
                     .filter(or_(Author2023DB.first_name.ilike(f"%{author}%"),
                                 Author2023DB.family_name.ilike(f"%{author}%"))
                             )
                     ).options(
                        joinedload(Enregistrement2023DB.reference)
                        .joinedload(ReferenceBibliographiqueLivre2023DB.authors)
                    )

    # valid = request.args.get("valid", "1")
    # if valid in ["1", "0"]:
    #     the_filtered_query = the_filtered_query.filter(Enregistrement2023DB.valide == int_to_bool(valid))
    #     the_total_query = the_total_query.filter(Enregistrement2023DB.valide == int_to_bool(valid))
    # else:
    #     the_filtered_query = the_filtered_query.filter(Enregistrement2023DB.valide == True)
    #     the_total_query = the_total_query.filter(Enregistrement2023DB.valide == True)

    filtered_total = the_filtered_query.count()
    total = the_total_query.count()
    logging.debug(filtered_total)
    return json_result(True, total=total, filtered_total=filtered_total), 200


@sat_biblio.route("/book-records-with-reference/search/", methods=["POST"])
def chercher_enregistrements_with_reference():
    data = request.get_json()
    the_query = Enregistrement2023DB.query
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
    if "aide_a_la_recherche" in data and data["aide_a_la_recherche"]:
        the_query.filter_by(aide_a_la_recherche=data["aide_a_la_recherche"])
        filtered = True
    # if "valide" in data and data["valide"]:
    #     the_query.filter_by(valide=data["valide"])
    #     filtered = True
    if filtered:
        results_db = the_query.all()
        results = [Enregistrement2023.from_db_to_data(res) for res in results_db]
        return json_result(True, results=results), 200
    else:
        return json_result(True, results=[]), 200


@sat_biblio.route("/book-records-with-reference/search-near/", methods=["GET"])
def chercher_enregistrements_proches_with_reference():
    query_result = request.args.get("record")
    res = []
    if re.match(r"^(A|B|C|D|MM|BBH|GHA|GHB|GHC|GHbr|BBC|CAF|JSFA|RCAF|Congrès|"
                r"RCNSS|CNSS|CSS|TAB|FAG|FAM|FAP|MML|NUM|NUMbr) [0-9]{1,5}.*", query_result):

        book_records_db = Enregistrement2023DB.query.filter(Enregistrement2023DB.cote.ilike(f"%{query_result}%")).all()

        for book_record_db in book_records_db:
            if book_record_db:
                res.append(dict(text=f"{book_record_db.reference.titre} {book_record_db.cote}",
                                value=book_record_db.id))
    else:
        book_records_db = db.session \
            .query(Enregistrement2023DB, ReferenceBibliographiqueLivre2023DB) \
            .filter(Enregistrement2023DB.id_reference == ReferenceBibliographiqueLivre2023DB.id) \
            .filter(ReferenceBibliographiqueLivre2023DB.titre.ilike(f"%{query_result}%"))
        for book_record_db, ref_biblio_db in book_records_db:
            res.append(dict(text=f"{book_record_db.reference.titre} {book_record_db.cote}",
                            value=book_record_db.id))

    return json_result(True, suggestedRecords=res), 200
# endregion


# region entries
@sat_biblio.route("/book-records-with-reference/<int:id_>/entries/", methods=["GET"])
def get_record_with_reference_entries(id_):
    n_page, size, sort_by = get_pagination(request)
    entry_type = request.args.get("type", "")
    entries = []
    if entry_type == "author":
        authors = Author2023.get_authors_by_record(id_, n_page, size, sort_by)
        entries.extend(authors)
    elif entry_type == "reference":
        references = ReferenceBibliographiqueLivre2023.get_references_by_record(id_, n_page, size, sort_by)
        entries.extend(references)
    return json_result(True, entries=entries), 200


@sat_biblio.route("/book-records-with-reference/<int:id_>/entries/count/", methods=["GET"])
def get_record_with_reference_count_entries(id_):
    entry_type = request.args.get("type", "")
    total = 0
    if entry_type == "author":
        author_count = Author2023.get_authors_by_record_count(id_)
        total += author_count
    elif entry_type == "reference":
        reference_count = ReferenceBibliographiqueLivre2023.get_references_by_record_count(id_)
        total += reference_count
    return json_result(True, total=total), 200
# endregion
