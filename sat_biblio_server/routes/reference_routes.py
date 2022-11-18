"""
Manages book references.
Book references are here
"""
import json

from flask import redirect, request, session

import logging

from sat_biblio_server.managers.log_manager import LogEventManager
from sat_biblio_server.routes.utils import get_pagination, int_to_bool
from sat_biblio_server.data.models import ReferenceBibliographiqueLivre, Author, Enregistrement, EmpruntLivre
from sat_biblio_server import sat_biblio
from sat_biblio_server.database import db, ReferenceBibliographiqueLivreDB
from sat_biblio_server.routes import validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result
import sat_biblio_server.data.validation as dv

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region références
@sat_biblio.route("/book-references/", methods=["GET", "POST"])
@validation_connexion_et_retour_defaut("email", ["POST"])
def book_references():
    if request.method == "POST":
        data = request.get_json()
        if dv.check_reference_bibliographique_livre(data):
            reference_db = ReferenceBibliographiqueLivre.from_data_to_db(data)
            db.session.add(reference_db)
            db.session.commit()
            LogEventManager(db).add_create_event(reference_db.id, session.get("id", -1),
                                                 ReferenceBibliographiqueLivreDB.__tablename__,
                                                 values=json.dumps(data))
            return json_result(True, id=reference_db.id, message="La référence a été sauvegardée"), 201
        return json_result(False, message="La sauvegarde de la référence a échoué."), 400
    elif request.method == "GET":
        n_page, size, sort_by = get_pagination(request)
        titre = request.args.get("titre", "")
        # print("titre", titre)

        the_query = ReferenceBibliographiqueLivreDB.query
        if titre:
            the_query = the_query.filter(ReferenceBibliographiqueLivreDB.titre.like(f"%{titre}%"))
        valid = request.args.get("valid", "1")
        # print(type(valid), valid)
        if valid in ["1", "0"]:
            # print("HERE")
            the_query = the_query.filter(ReferenceBibliographiqueLivreDB.valide == int_to_bool(valid))
        else:
            the_query = the_query.filter(ReferenceBibliographiqueLivreDB.valide == True)

        # sort_desc = request.args.get("sortDesc")
        # references = [{"first_name": author.first_name,
        #             "family_name": author.family_name,
        #             "id": author.id}
        #            for author in ReferenceBibliographiqueLivreDB
        #            .query.order_by(sort_by).paginate(page=n_page, per_page=size).items]
        if sort_by:
            the_query = the_query.order_by(sort_by)
        else:
            the_query = the_query.order_by("title")

        references = []
        for reference_db in the_query.paginate(page=n_page, per_page=size).items:
            reference = ReferenceBibliographiqueLivre.from_db_to_data(reference_db)
            reference["authors"] = " ".join(
                [f"{author['first_name']} {author['family_name']}" for author in reference['authors']])
            references.append(reference)
        logging.debug(len(references))
        return json_result(True, references=references), 200


@sat_biblio.route("/book-references/<int:id_>/", methods=["GET", "PUT", "DELETE"])
@validation_connexion_et_retour_defaut("email", ["PUT", "DELETE"])
def book_reference(id_):
    if request.method == "GET":
        ref_livre_db = ReferenceBibliographiqueLivre.from_id_to_db(id_)
        if ref_livre_db:
            logging.warning(Author.get_authors_by_ref(id_, 1, 10, ""))
            logging.warning(Enregistrement.get_records_by_ref(id_, 1, 10, ""))
            ref_livre = ReferenceBibliographiqueLivre.from_db_to_data(ref_livre_db)
            if ref_livre:
                ref_livre["authors"] = [
                    {"text": f"{author_db.first_name} {author_db.family_name}", "value": author_db.id}
                    for author_db in ref_livre_db.authors]
                logging.debug(ref_livre)
                return json_result(True, reference=ref_livre), 200
            else:
                logging.error("reference void")
                return json_result(False), 404
        return json_result(False), 404
    elif request.method == "PUT":
        data = request.get_json()
        ref_biblio_db = ReferenceBibliographiqueLivre.from_id_to_db(id_)
        if ref_biblio_db:
            previous_value = ReferenceBibliographiqueLivre.from_db_to_data(ref_biblio_db)

            auteurs_db = []
            for auteur in data["auteurs"]:
                if "value" in auteur:
                    author_db = Author.from_id_to_db(auteur["value"])
                    if author_db:
                        auteurs_db.append(author_db)
            ref_biblio_db.authors = auteurs_db
            ref_biblio_db.titre = data["titre"]
            ref_biblio_db.lieu_edition = data["lieu_edition"]
            ref_biblio_db.editeur = data["editeur"]
            ref_biblio_db.annee = data["annee"]
            ref_biblio_db.nd_page = data["nb_page"]

            db.session.commit()
            LogEventManager(db).add_update_event(ref_biblio_db.id, session.get("id", -1),
                                                 ReferenceBibliographiqueLivreDB.__tablename__,
                                                 values=json.dumps(dict(
                                                     previous=previous_value,
                                                     new=ReferenceBibliographiqueLivre.from_db_to_data(ref_biblio_db))))

            return json_result(True), 200
        return json_result(False), 404
    elif request.method == "DELETE":
        ref_biblio_db = ReferenceBibliographiqueLivreDB.query.filter_by(id=id_).first()
        if ref_biblio_db:
            db.session.delete(ref_biblio_db)
            db.session.commit()
            LogEventManager.add_delete_event(ref_biblio_db.id, session.get("id", -1),
                                             ReferenceBibliographiqueLivreDB.__tablename__,
                                             values=json.dumps(
                                                 ReferenceBibliographiqueLivre.from_db_to_data(ref_biblio_db)))
            return json_result(True), 204
        return json_result(False), 404


@sat_biblio.route("/book-references/count/", methods=["GET"])
def book_references_count():
    titre = request.args.get("titre", "")
    the_filtered_query = ReferenceBibliographiqueLivreDB.query
    the_total_query = ReferenceBibliographiqueLivreDB.query
    if titre:
        the_filtered_query = the_filtered_query.filter(ReferenceBibliographiqueLivreDB.titre.like(f"%{titre}%"))

    valid = request.args.get("valid", "1")
    if valid in ["1", "0"]:
        the_filtered_query = the_filtered_query.filter(ReferenceBibliographiqueLivreDB.valide == int_to_bool(valid))
        the_total_query = the_total_query.filter(ReferenceBibliographiqueLivreDB.valide == int_to_bool(valid))
    else:
        the_filtered_query = the_filtered_query.filter(ReferenceBibliographiqueLivreDB.valide == True)
        the_total_query = the_total_query.filter(ReferenceBibliographiqueLivreDB.valide == True)

    filtered_count = the_filtered_query.count()
    total = the_total_query.count()
    logging.debug(filtered_count)
    return json_result(True, total=total, filtered_total=filtered_count), 200


@sat_biblio.route("/book-references/search-near/", methods=["GET"])
def chercher_reference_livre_plus_proches():
    titre = request.args.get("titre")
    references_db = ReferenceBibliographiqueLivreDB.query \
        .filter(ReferenceBibliographiqueLivreDB.titre.like(f"%{titre}%")).all()
    references = []
    for reference_db in references_db:
        # reference = ReferenceBibliographiqueLivre.from_db_to_data(reference_db)
        references.append({"text": reference_db.titre,
                           "value": reference_db.id})
    return json_result(True, suggestedReferences=references), 200


@sat_biblio.route("/book-references/search/", methods=["POST"])
def chercher_reference_livre():
    data = request.get_json()
    the_query = ReferenceBibliographiqueLivreDB.query
    if data is None:
        return json_result(False), 400
    if "titre" in data and data["titre"]:
        the_query = the_query.filter(ReferenceBibliographiqueLivreDB.titre.like(f"%{data['titre']}%"))
        ref_livres_db = the_query.all()
        results = [ReferenceBibliographiqueLivre.from_db_to_data(ref_livre_db)
                   for ref_livre_db in ref_livres_db]
        return json_result(True, results=results)
    return json_result(True, results=[]), 200
# endregion


# region entries
@sat_biblio.route("/book-references/<int:id_>/entries/", methods=["GET"])
def get_reference_entries(id_):
    n_page, size, sort_by = get_pagination(request)
    entries = []
    authors = Author.get_authors_by_ref(id_, n_page, size, sort_by)
    records = Enregistrement.get_records_by_author(id_, n_page, size, sort_by)
    entries.extend(authors)
    entries.extend(records)
    return json_result(True, entries=entries), 200


@sat_biblio.route("/book-references/<int:id_>/entries/count/", methods=["GET"])
def get_reference_count_entries(id_):
    author_count = Author.get_authors_by_ref_count(id_)
    record_count = Enregistrement.get_records_by_author_count(id_)
    total = author_count + record_count
    return json_result(True, total=total)


@sat_biblio.route("/book-references/<int:id_>/borrowings/current/", methods=["GET"])
# @validation_connexion_et_retour_defaut("email", ["GET"])
def get_current_borrowing_state_of_book_reference(id_):
    is_being_borrowed = EmpruntLivre.is_book_being_borrowed(id_)
    return json_result(True, is_being_borrowed=is_being_borrowed)


@sat_biblio.route("/book-references/<int:id_>/borrowings/", methods=["GET"])
# @validation_connexion_et_retour_defaut("email", ["GET"])
def get_all_borrowing_state_of_book_reference(id_):
    borrowings = EmpruntLivre.get_all_book_borrowings(id_)
    return json_result(True, borrowings=borrowings)
# endregion
