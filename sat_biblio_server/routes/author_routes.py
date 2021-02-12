"""
Manages authors.

Authors have only a first name and family name.
"""

from flask import redirect, jsonify, request

import logging

from sqlalchemy import or_

from sat_biblio_server.data.models import Author
from sat_biblio_server.database import db, AuthorDB
from sat_biblio_server import sat_biblio
from sat_biblio_server.routes import validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result
import sat_biblio_server.data.validation as dv

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region auteur

# @sat_biblio.route("/api/auteur/creer", methods=["POST"])
@sat_biblio.route("/auteurs/", methods=["POST", "GET"])
@validation_connexion_et_retour_defaut("email", redirect("/api"))
def auteurs():
    """
    POST: add an author
    GET: get list of authors
    :return:
    """
    if request.method == "GET":
        n_page = int(request.args.get("page"))
        size = int(request.args.get("size"))
        sort_by = request.args.get("sortBy")

        the_query = AuthorDB.query
        # sort_desc = request.args.get("sortDesc")
        # region filtre
        first_name = request.args.get("first_name", "")
        family_name = request.args.get("family_name", "")
        if first_name:
            the_query = the_query.filter(AuthorDB.first_name.like(f"%{first_name}%"))
        if family_name:
            the_query = the_query.filter(AuthorDB.family_name.like(f"%{family_name}%"))
        # endregion
        authors = [{"first_name": author.first_name,
                    "family_name": author.family_name,
                    "id": author.id}
                   for author in the_query.order_by(sort_by).paginate(page=n_page, per_page=size).items]
        logging.debug(len(authors))
        return json_result(True, authors=authors)
    elif request.method == "POST":
        data = request.get_json()
        if dv.check_author(data):
            author = AuthorDB(first_name=data["first_name"],
                              family_name=data["family_name"])
            db.session.add(author)
            db.session.commit()
            return json_result(True)
        else:
            return jsonify(False)


@sat_biblio.route("/api/auteurs/<int:id_>", methods=["GET", "PUT", "DELETE"])
@validation_connexion_et_retour_defaut("email", redirect("/"))
def lire_auteur(id_):
    """
    GET: read an author
    PUT: update an author

    :param id_:
    :return:
    """

    if request.method == "GET":
        author_db = AuthorDB.query.filter_by(id=id_).first()
        author = Author.from_db_to_data(author_db)
        return json_result(True, author=author)
    elif request.method == "POST":
        data = request.get_json()
        author = AuthorDB.query.filter_by(id=id_).first()
        author.first_name = data["first_name"]
        author.family_name = data["family_name"]
        db.session.commit()
        return json_result(True)
    elif request.method == "DELETE":
        id_author = id_
        author_db = AuthorDB.query.filter_by(id=id_author).first()
        # exists ReferenceBibliographiqueLivreDB.query.filter_by(au)
        # TODO refuser si c'est utilisé dans des références
        if author_db:
            db.session.delete(author_db)
            db.session.commit()
        return jsonify({"success": True, })


@sat_biblio.route("/api/auteur/chercher-proches", methods=["GET", "POST"])
def chercher_auteurs_plus_proches():
    query_result = request.args.get("auteur")

    authors_db = AuthorDB.query.filter(
        or_(AuthorDB.first_name.like(f"%{query_result}%"),
            AuthorDB.family_name.like(f"%{query_result}%"))
    ).all()

    res = [{"text": f"{author_db.first_name} {author_db.family_name}", "value": author_db.id}
           for author_db in authors_db]
    return json_result(True, suggestedAuthors=res)


@sat_biblio.route("/api/auteur/chercher", methods=["POST"])
def chercher_auteurs():
    data = request.get_json()
    the_query = AuthorDB.query
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
    results = [Author.from_db_to_data(author_db) for author_db in results]
    return json_result(True, results=results)


# @sat_biblio.route("/api/auteur/liste", methods=["GET"])
# def listes_auteurs():
#     pass


@sat_biblio.route("/api/auteur/nombre", methods=["GET"])
def get_author_total_number():
    the_query = AuthorDB.query
    # region filtre
    first_name = request.args.get("first_name", "")
    family_name = request.args.get("family_name", "")

    if first_name:
        the_query = the_query.filter(AuthorDB.first_name.like(f"%{first_name}%"))
    if family_name:
        the_query = the_query.filter(AuthorDB.family_name.like(f"%{family_name}%"))
    # endregion
    number = the_query.count()
    logging.debug(number)
    return json_result(True, number=number)
# endregion
