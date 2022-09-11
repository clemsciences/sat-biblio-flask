"""
"""
import logging

from flask import request

from sat_biblio_server.managers.bnf_sru_manager import BnfSruManager, RequestResult
from sat_biblio_server.managers.log_manager import LogEventManager
from sat_biblio_server.routes.utils import get_pagination, int_to_bool
from sat_biblio_server.data import validation
from sat_biblio_server.data.models import Author, ReferenceBibliographiqueLivre, Enregistrement
from sat_biblio_server.database import db, AuthorDB
from sat_biblio_server import sat_biblio, ReferenceBibliographiqueLivreDB
from sat_biblio_server.routes import validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result
import sat_biblio_server.data.validation as dv

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


@sat_biblio.route("/dublin-core/", methods=["GET"])
def dublin_core_request():
    """
    GET: get list of dublin core entries
    :return:
    """
    if request.method == "GET":
        query = request.args.get("query", "")
        n_page, size, sort_by = get_pagination(request)
        print(f"query {query}")

        entries = BnfSruManager.search_from_query(query)
        print(entries.number_of_records)
        if entries:
            assert isinstance(entries, RequestResult)
            print("1")
            # print(entries.to_dict())

            return json_result(True, entries=entries.to_dict(), total=int(entries.number_of_records)), 200
        print("2")
        return json_result(True, entries=[], total=0), 200
    print("3")
    return json_result(False), 400


@sat_biblio.route("/dublin-core/<string:naan>/<string:ark_name>", methods=["GET"])
def dublin_core_entry_request(naan, ark_name):
    """
    GET: get entry of dublin core
    :return:
    """
    if request.method == "GET":
        n_page, size, sort_by = get_pagination(request)

        the_query = AuthorDB.query
        # sort_desc = request.args.get("sortDesc")
        # region filter
        first_name = request.args.get("first_name", "")
        if first_name:
            the_query = the_query.filter(AuthorDB.first_name.like(f"%{first_name}%"))
            logging.error(f"{first_name}")
        family_name = request.args.get("family_name", "")
        if family_name:
            the_query = the_query.filter(AuthorDB.family_name.like(f"%{family_name}%"))
            logging.error(f"{family_name}")
        valid = request.args.get("valid", "1")
        if valid in ["1", "0"]:
            the_query = the_query.filter(AuthorDB.valide == int_to_bool(valid))
        else:
            the_query = the_query.filter(AuthorDB.valide == True)

        if sort_by:
            the_query = the_query.order_by(sort_by)
        else:
            the_query = the_query.order_by("family_name")

        authors = [Author.from_db_to_data(author)
                   for author in the_query.paginate(page=n_page, per_page=size).items]
        logging.error(len(authors))
        return json_result(True, authors=authors), 200
    return json_result(False), 400
