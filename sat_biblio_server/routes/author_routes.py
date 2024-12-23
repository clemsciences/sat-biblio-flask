"""
Manages authors.

Authors have only a first name and family name.
"""
import json
import logging
from urllib.parse import urlparse

from flask import redirect, request, session
from sqlalchemy import or_, and_

from sat_biblio_server.managers.log_manager import LogEventManager
from sat_biblio_server.routes.utils import get_pagination, int_to_bool
from sat_biblio_server.data import validation
# from sat_biblio_server.data.models import Author, ReferenceBibliographiqueLivre, Enregistrement
from sat_biblio_server.data.models_2023 import Author2023, ReferenceBibliographiqueLivre2023, Enregistrement2023
from sat_biblio_server.database import db
from sat_biblio_server import sat_biblio, ReferenceBibliographiqueLivre2023DB, Author2023DB
from sat_biblio_server.routes import validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result
import sat_biblio_server.data.validation as dv

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region auteur

# @sat_biblio.route("/api/auteur/creer", methods=["POST"])
@sat_biblio.route("/authors/", methods=["POST", "GET"])
@validation_connexion_et_retour_defaut("email", ["POST"])
def authors_():
    """
    POST: add an author
    GET: get list of authors
    :return:
    """
    if request.method == "GET":
        n_page, size, sort_by = get_pagination(request)

        the_query = Author2023DB.query
        # sort_desc = request.args.get("sortDesc")
        # region filter
        first_name = request.args.get("first_name", "")
        if first_name:
            the_query = the_query.filter(Author2023DB.first_name.like(f"%{first_name}%"))
            logging.error(f"{first_name}")
        family_name = request.args.get("family_name", "")
        if family_name:
            the_query = the_query.filter(Author2023DB.family_name.like(f"%{family_name}%"))
            logging.error(f"{family_name}")
        # valid = request.args.get("valid", "1")
        # if valid in ["1", "0"]:
        #     the_query = the_query.filter(Author2023DB.valide == int_to_bool(valid))
        # else:
        # the_query = the_query.filter(Author2023DB.valide == True)

        if sort_by:
            the_query = the_query.order_by(sort_by)
        else:
            the_query = the_query.order_by("family_name")

        authors = [Author2023.from_db_to_data(author)
                   for author in the_query.paginate(page=n_page, per_page=size).items]
        logging.error(len(authors))
        return json_result(True, authors=authors), 200
    elif request.method == "POST":
        data = request.get_json()

        if dv.check_author(data):
            author_exists = Author2023DB.query.filter_by(first_name=data["first_name"],
                                                     family_name=data["family_name"]).first()
            if not author_exists:
                author_db = Author2023.from_data_to_db(data)
                db.session.add(author_db)
                db.session.commit()
                LogEventManager(db).add_create_event(author_db.id, session.get("id", -1), Author2023DB.__tablename__,
                                                 values=json.dumps(data))
                return json_result(True, "Ajout de l'auteur correctement effectué.", id=author_db.id), 201
            return json_result(True, "L'auteur existe déjà.", id=author_exists.id), 200
        else:
            return json_result(False), 304


@sat_biblio.route("/authors/<int:id_>/", methods=["GET", "PUT", "DELETE"])
@validation_connexion_et_retour_defaut("email", ["DELETE", "PUT"])
def author_(id_):
    """
    GET: read an author
    PUT: update an author
    DELETE: delete an author

    :param id_:
    :return:
    """

    if request.method == "GET":
        author_db = Author2023DB.query.filter_by(id=id_).first()
        author = Author2023.from_db_to_data(author_db)
        # logging.warning("ref")
        # logging.warning(ReferenceBibliographiqueLivre.get_references_by_author(id_, 1, 10, ""))
        # logging.warning("enregistrement")
        # logging.warning(Enregistrement.get_records_by_author(id_, 1, 10, ""))

        return json_result(True, author=author), 200
    elif request.method == "PUT":
        data = request.get_json()
        author = Author2023DB.query.filter_by(id=id_).first()
        previous_value = Author2023.from_db_to_data(author)
        if validation.check_author(data):

            author.first_name = data["first_name"]
            author.family_name = data["family_name"]
            db.session.commit()
            LogEventManager(db).add_update_event(id_, session.get("id", -1), Author2023DB.__tablename__,
                                                 values=json.dumps(dict(previous=previous_value, new=data)))
            return json_result(True, "Auteur correctement mis à jour."), 200
        else:
            return json_result(False, "Echec de la mise à jour de l'auteur."), 400
    elif request.method == "DELETE":
        id_author = id_
        author_db = Author2023DB.query.filter_by(id=id_author).first()
        # exists ReferenceBibliographiqueLivreDB.query.filter_by(au)
        # TODO refuser si c'est utilisé dans des références
        if author_db:
            author_data = Author2023.from_db_to_data(author_db)
            db.session.delete(author_db)
            db.session.commit()
            LogEventManager(db).add_delete_event(author_db.id, session.get("id", -1), Author2023DB.__tablename__,
                                             values=json.dumps(author_data))
            return json_result(True), 204
        return json_result(False), 400


@sat_biblio.route("/authors/count/", methods=["GET"])
def authors_count():
    """

    :return:
    """
    the_filtered_query = Author2023DB.query
    # region filtre
    if "first_name" in request.args:
        the_filtered_query = the_filtered_query.filter(Author2023DB.first_name.like(f"%{request.args.get('first_name')}%"))

    if "family_name" in request.args:
        the_filtered_query = the_filtered_query.filter(Author2023DB.family_name.like(f"%{request.args.get('family_name')}%"))
    # endregion
    # query = """
    # SELECT *
    # FROM Author AS A
    # WHERE A.first_name LIKE '%s' AND A.family_name LIKE '%s' AND 1 = (
    #     SELECT valid
    #     FROM ReferenceBibliographiqueLivre AS RBL
    #     WHERE A.id = RBL.
    # )
    # """

    the_total_query = Author2023DB.query.filter()


    # valid = request.args.get("valid", "1")
    # if valid in ["1", "0"]:
    #     print("HERE")
    #    the_filtered_query = the_filtered_query.filter(Author2023DB.valide == int_to_bool(valid))
    #    the_total_query = the_total_query.filter(Author2023DB.valide == int_to_bool(valid))
    # else:
    # the_filtered_query = the_filtered_query.filter(Author2023DB.valide == True)
    # the_total_query = the_total_query.filter(Author2023DB.valide == True)

    filtered_total = the_filtered_query.count()
    total = the_total_query.count()
    # logging.debug(f"{filtered_total}/{total}")
    return json_result(True, total=total, filtered_total=filtered_total), 200


@sat_biblio.route("/authors/search-near/", methods=["GET"])
def chercher_auteurs_plus_proches():
    author_query_result = request.args.get("auteur", "").strip()
    first_name_query = request.args.get("first_name", "").strip()
    family_name_query = request.args.get("family_name", "").strip()
    exact_matching = False

    authors_db = set()
    if first_name_query and family_name_query:
        res_authors_db = set(Author2023DB.query.filter(
            and_(Author2023DB.first_name.like(f"%{first_name_query}%"),
                 Author2023DB.family_name.like(f"%{family_name_query}%"))
        ).all())
        authors_db.update(res_authors_db)
    elif first_name_query:
        res_authors_db = set(Author2023DB.query.filter(
            Author2023DB.first_name.like(f"%{first_name_query}%")
        ).all())
        authors_db.update(res_authors_db)
    elif family_name_query:
        res_authors_db = set(Author2023DB.query.filter(
            Author2023DB.family_name.like(f"%{family_name_query}%")
        ).all())
        authors_db.update(res_authors_db)
    if first_name_query and family_name_query:
        exact_matching = ((Author2023DB.query
                          .filter_by(first_name=first_name_query)
                          .filter_by(family_name=family_name_query))
                          .first()) is not None
    if author_query_result:
        queries_string = author_query_result.split(" ")
        for query_string in queries_string:
            res_authors_db = set(Author2023DB.query.filter(
                or_(Author2023DB.first_name.like(f"%{query_string}%"),
                    Author2023DB.family_name.like(f"%{query_string}%"))
            ).all())
            authors_db.update(res_authors_db)
    res = []
    for author_db in authors_db:
        res.append(dict(text=f"{author_db.first_name} {author_db.family_name}",
                        value=author_db.id,
                        family_name=author_db.family_name,
                        first_name=author_db.first_name))
    return json_result(True, suggestedAuthors=res, exactMatching=exact_matching), 200


@sat_biblio.route("/authors/search/", methods=["POST"])
def chercher_auteurs():
    data = request.get_json()
    the_query = Author2023DB.query
    filtered = False
    if "first_name" in data and data["first_name"]:
        the_query = the_query.filter_by(first_name=data["first_name"])
        filtered = True
    if "family_name" in data and data["family_name"]:
        the_query = the_query.filter_by(family_name=data["family_name"])
        filtered = True
    if filtered:
        results = the_query.all()
    else:
        results = []
    results = [Author2023.from_db_to_data(author_db) for author_db in results]
    return json_result(True, results=results), 200


# endregion

# region entries
@sat_biblio.route("/authors/<int:id_>/entries/")
def author_entries_routes(id_):
    n_page, size, sort_by = get_pagination(request)
    entry_type = request.args.get("type", "")
    entries = []
    if entry_type == "record":
        records = Enregistrement2023.get_records_by_author(id_, n_page, size, sort_by)
        entries.extend(records)
    elif entry_type == "reference":
        references = ReferenceBibliographiqueLivre2023.get_references_by_author(id_, n_page, size, sort_by)
        entries.extend(references)
    return json_result(True, entries=entries), 200


@sat_biblio.route("/authors/<int:id_>/entries/count/", methods=["GET"])
def author_entries_count_routes(id_):
    # logging.warning("bizarre")
    entry_type = request.args.get("type", "")
    total = 0
    if entry_type == "record":
        record_count = Enregistrement2023.get_records_by_author_count(id_)
        total += record_count
    elif entry_type == "reference":
        reference_count = ReferenceBibliographiqueLivre2023.get_references_by_author_count(id_)
        total += reference_count

    return json_result(True, total=total), 200


@sat_biblio.route("/authors/without-reference")
def authors_without_reference_route():
    authors = []
    # TODO
    return json_result(True, authors=authors), 200
# endregion
