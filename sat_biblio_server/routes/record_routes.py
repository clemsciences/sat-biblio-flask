"""
Manages records in library.

Records are hints to manage books in the library.
"""
import json
import logging
import re

from flask import request, session
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

import sat_biblio_server.data.validation as dv
from sat_biblio_server import sat_biblio, Author2023DB
from sat_biblio_server.data.models_2023 import Enregistrement2023, ReferenceBibliographiqueLivre2023, Author2023
from sat_biblio_server.database import db, ReferenceBibliographiqueLivre2023DB, \
    Enregistrement2023DB
from sat_biblio_server.managers.log_manager import LogEventManager
from sat_biblio_server.routes import get_pagination, validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region enregistrement
@sat_biblio.route("/book-records/", methods=["GET", "POST"])
@validation_connexion_et_retour_defaut("email", ["POST", "PUT"])
def book_records():
    if request.method == "POST":
        data = request.get_json()
        if dv.check_enregistrement(data):
            enregistrement_db = Enregistrement2023.from_data_to_db(data)
            db.session.add(enregistrement_db)
            db.session.commit()
            LogEventManager(db).add_create_event(enregistrement_db.id, session.get("id", -1),
                                                 Enregistrement2023DB.__tablename__,
                                                 values=json.dumps(
                                                     Enregistrement2023.from_db_to_data(enregistrement_db)))
            return json_result(True, id=enregistrement_db.id,
                               message="L'enregistrement a correctement été sauvegardé."), 201
        return json_result(False, message="Erreur de la sauvegarde de l'enregistrement."), 400
    elif request.method == "GET":
        n_page, size, sort_by, sort_desc = get_pagination(request)

        # region filtre
        cote = request.args.get("cote", "")
        titre = request.args.get("titre", "")
        mot_clef = request.args.get("mot_clef", "")
        author = request.args.get("author", "")

        the_query = Enregistrement2023DB.query
        if cote:
            the_query = the_query.filter(Enregistrement2023DB.cote.like(f"%{cote}%"))
        if titre:
            the_query = the_query.join(ReferenceBibliographiqueLivre2023DB) \
                .filter(ReferenceBibliographiqueLivre2023DB.titre.like(f"%{titre}%"))
        if mot_clef:
            the_query = the_query.filter(Enregistrement2023DB.aide_a_la_recherche.like(f"%{mot_clef}%"))
        if author:
            the_query = (the_query
                         .join(ReferenceBibliographiqueLivre2023DB)
                         .join(ReferenceBibliographiqueLivre2023DB.authors)
                         .filter(or_(Author2023DB.first_name.ilike(f"%{author}%"),
                                     Author2023DB.family_name.ilike(f"%{author}%"),
                                     (Author2023DB.first_name + ' ' + Author2023DB.family_name).ilike(
                                         f"%{author}%"),
                                     (Author2023DB.family_name + ' ' + Author2023DB.first_name).ilike(
                                         f"%{author}%")
                                     )
                                 )
                         ).options(
                joinedload(Enregistrement2023DB.reference)
                .joinedload(ReferenceBibliographiqueLivre2023DB.authors)
            )
        # valid = request.args.get("valid", "1")
        # if valid in ["1", "0"]:
        #     the_query = the_query.filter(Enregistrement2023DB.valide == int_to_bool(valid))
        # else:
        #     the_query = the_query.filter(Enregistrement2023DB.valide == True)
        # endregion

        if sort_by:
            if sort_by == "cote":
                field = Enregistrement2023DB.cote
            elif sort_by == "annee_obtention":
                field = Enregistrement2023DB.annee_obtention
            elif sort_by == "date_derniere_modification":
                field = Enregistrement2023DB.date_derniere_modification
            else:
                field = Enregistrement2023DB.cote

            if sort_desc:
                the_query = the_query.order_by(field.desc(), Enregistrement2023DB.id.desc())
            else:
                the_query = the_query.order_by(field.asc(), Enregistrement2023DB.id.asc())
        elif sort_desc:
            the_query = the_query.order_by(Enregistrement2023DB.cote.desc(), Enregistrement2023DB.id.desc())
        else:
            the_query = the_query.order_by(Enregistrement2023DB.cote.asc(), Enregistrement2023DB.id.asc())

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


@sat_biblio.route("/book-records/<int:id_>/", methods=["GET", "DELETE", "PUT"])
@validation_connexion_et_retour_defaut("email", ["DELETE", "PUT"])
def book_record(id_):
    if request.method == "GET":
        # TODO valide?
        enregistrement_db = Enregistrement2023DB.query.filter_by(id=id_).first()
        if enregistrement_db:
            logging.warning(ReferenceBibliographiqueLivre2023.get_references_by_record(id_, 1, 10, ""))
            # logging.warning(Author.get_authors_by_record(id_, 1, 10, ""))
            enregistrement = Enregistrement2023.from_db_to_data(enregistrement_db)
            reference_db = ReferenceBibliographiqueLivre2023DB.query.filter_by(id=enregistrement_db.reference.id).first()
            if reference_db:
                enregistrement["reference"] = ReferenceBibliographiqueLivre2023.from_db_to_data(reference_db)
                enregistrement["reference"]["text"] = enregistrement_db.reference.titre
                enregistrement["reference"]["value"] = enregistrement_db.id_reference
            return json_result(True, enregistrement=enregistrement), 200
        return json_result(False), 404
    elif request.method == "DELETE":
        enregistrement_db = Enregistrement2023DB.query.filter_by(id=id_).first()
        if enregistrement_db:
            record_data = Enregistrement2023.from_db_to_data(enregistrement_db)
            db.session.delete(enregistrement_db)
            db.session.commit()
            LogEventManager(db).add_delete_event(enregistrement_db.id, session.get("id", -1),
                                                 Enregistrement2023DB.__tablename__,
                                                 values=json.dumps(record_data))  # TODO
            return json_result(True), 204
        else:
            return json_result(False), 404
    elif request.method == "PUT":
        data = request.get_json()
        enregistrement_db = Enregistrement2023DB.query.filter_by(id=id_).first()
        if enregistrement_db:
            previous_value = Enregistrement2023.from_db_to_data(enregistrement_db)
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
            if "aide_a_la_recherche" in data:
                enregistrement_db.aide_a_la_recherche = data["aide_a_la_recherche"]
            db.session.commit()

            LogEventManager(db).add_update_event(id_,
                                                 session.get("id", -1),
                                                 Enregistrement2023DB.__tablename__,
                                                 values=json.dumps(dict(previous=previous_value,
                                                                        new=Enregistrement2023.from_db_to_data(
                                                                            enregistrement_db))))
            return json_result(True, "Enregistrement correctement mis à jour."), 200
        return json_result(False, "Echec de la mis à jour de l'enregistrement."), 404


@sat_biblio.route("/book-records/count/", methods=["GET"])
def book_records_count():
    cote = request.args.get("cote", "")
    titre = request.args.get("titre", "")
    mot_clef = request.args.get("mot_clef", "")
    author = request.args.get("author", "")

    the_filtered_query = Enregistrement2023DB.query
    the_total_query = Enregistrement2023DB.query
    if cote:
        the_filtered_query = the_filtered_query.filter(Enregistrement2023DB.cote.like(f"%{cote}%"))
    if titre:
        the_filtered_query = the_filtered_query.join(ReferenceBibliographiqueLivre2023DB) \
            .filter(ReferenceBibliographiqueLivre2023DB.titre.like(f"%{titre}%"))
    if mot_clef:
        the_filtered_query = the_filtered_query.filter(Enregistrement2023DB.aide_a_la_recherche.like(f"%{mot_clef}%"))
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


@sat_biblio.route("/book-records/search-near/", methods=["GET"])
def chercher_enregistrements_proches():
    query_result = request.args.get("record")
    res = []
    if re.match(r"^(A|B|C|D|MM|BBH|GHA|GHB|GHC|GHbr|BBC|CAF|JSFA|RCAF|Congrès|"
                r"RCNSS|CNSS|CSS|TAB|FAG|FAM|FAP|MML|NUM|NUMbr) [0-9]{1,5}.*", query_result):

        book_records_db = Enregistrement2023DB.query.filter(Enregistrement2023DB.cote.like(f"%{query_result}%")).all()

        for book_record_db in book_records_db:
            if book_record_db:
                res.append(dict(text=f"{book_record_db.reference.titre} {book_record_db.cote}",
                                value=book_record_db.id))
    else:
        book_records_db = db.session \
            .query(Enregistrement2023DB, ReferenceBibliographiqueLivre2023DB) \
            .filter(Enregistrement2023DB.id_reference == ReferenceBibliographiqueLivre2023DB.id) \
            .filter(ReferenceBibliographiqueLivre2023DB.titre.like(f"%{query_result}%"))
        for book_record_db, ref_biblio_db in book_records_db:
            res.append(dict(text=f"{book_record_db.reference.titre} {book_record_db.cote}",
                            value=book_record_db.id))

    return json_result(True, suggestedRecords=res), 200


@sat_biblio.route("/book-records/keywords/", methods=["GET"])
def get_all_keywords():
    all_keywords_raw = db.session.query(Enregistrement2023DB.aide_a_la_recherche).filter(Enregistrement2023DB.aide_a_la_recherche != "").all()
    keywords_count = {}
    for row in all_keywords_raw:
        if row[0]:
            # On suppose ici que les mots clés sont séparés par un ou plusieurs espaces
            # car l'aperçu sqlite montrait des double espaces ou espaces simples.
            parts = [p.strip() for p in re.split(r'\s+', row[0]) if p.strip()]
            for p in parts:
                keywords_count[p] = keywords_count.get(p, 0) + 1
    
    # On renvoie une liste d'objets avec le mot clé et sa fréquence
    keywords_list = [{"text": k, "count": v} for k, v in keywords_count.items()]
    return json_result(True, keywords=keywords_list), 200


# endregion


# region entries
@sat_biblio.route("/book-records/<int:id_>/entries/", methods=["GET"])
def get_record_entries(id_):
    n_page, size, sort_by, sort_desc = get_pagination(request)
    entry_type = request.args.get("type", "")
    entries = []
    if entry_type == "author":
        authors = Author2023.get_authors_by_record(id_, n_page, size, sort_by)
        entries.extend(authors)
    elif entry_type == "reference":
        references = ReferenceBibliographiqueLivre2023.get_references_by_record(id_, n_page, size, sort_by)
        entries.extend(references)
    return json_result(True, entries=entries), 200


@sat_biblio.route("/book-records/<int:id_>/entries/count/", methods=["GET"])
def get_record_count_entries(id_):
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
