"""
Retrieve resources by ARK name.

Resources are:
- authors,
- book references,
- record.
"""

import logging

from flask import request

from sat_biblio_server.managers.ark_manager import ArkManager
from sat_biblio_server import sat_biblio
from sat_biblio_server.utils import json_result

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


@sat_biblio.route(f"/ark:/<string:naan>/<string:ark_name>", methods=["GET", "POST"])
def ark_name_resolver_route(naan: str, ark_name: str):
    if request.method == "GET":
        if naan == ArkManager.AUTHORITY:
            reconstructed_ark_name = f"{naan}/{ark_name}"
            resource = ArkManager.get_resource(reconstructed_ark_name)
            if resource:
                return json_result(True, **resource)
            # record_db = Enregistrement2023DB.query.filter_by(ark_name=reconstructed_ark_name).first()
            # if record_db:
            #     return json_result(True, id=record_db.id, table_name=Enregistrement2023DB.__tablename__), 200
            # book_reference_db = ReferenceBibliographiqueLivre2023DB.query.filter_by(ark_name=reconstructed_ark_name).first()
            # if book_reference_db:
            #     return json_result(True, id=book_reference_db, table_name=ReferenceBibliographiqueLivre2023DB.__tablename__), 200
            # author_db = Author2023DB.query.filter_by(ark_name=reconstructed_ark_name).first()
            # if author_db:
            #     return json_result(True, id=author_db.id, table_name=Author2023DB.__tablename__)
            return json_result(True, id=-1)

        return json_result(False, message="hoho"), 404
    logging.error(f"{naan}/{ark_name}")
    return json_result(False, message=f"{naan}-{ark_name}"), 400


@sat_biblio.route("/ark/generate-for-all-entries-missing-ark/", methods=["GET"])
def generate_ark_for_all_entries_missing_ones_route():
    ArkManager.give_ark_names()
    return json_result(True, message="Succès")
