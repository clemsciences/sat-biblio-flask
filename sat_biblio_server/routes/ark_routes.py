"""
Retrieve resources by ARK name.

Resources are:
- authors,
- book references,
- record.
"""

import logging

from flask import request
from sat_biblio_server import sat_biblio
from sat_biblio_server.data.models_2023 import Enregistrement2023, ReferenceBibliographiqueLivre2023, Author2023
from sat_biblio_server.database import ReferenceBibliographiqueLivre2023DB, \
    Enregistrement2023DB, Author2023DB
from sat_biblio_server.utils import json_result

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


@sat_biblio.route(f"/ark:/<naan:string>/<ark_name:string>", methods=["GET", "POST"])
def book_records(naan: str, ark_name: str):
    if request.method == "GET":
        enregistrement_db = Enregistrement2023DB.query.filter_by(ark=ark_name).first()
        if enregistrement_db:
            logging.warning(ReferenceBibliographiqueLivre2023.get_references_by_record(id_, 1, 10, ""))
            # logging.warning(Author.get_authors_by_record(id_, 1, 10, ""))
            enregistrement = Enregistrement2023.from_db_to_data(enregistrement_db)
            reference_db = ReferenceBibliographiqueLivre2023DB.query.filter_by(
                id=enregistrement_db.reference.id).first()
            if reference_db:
                enregistrement["reference"] = ReferenceBibliographiqueLivre2023.from_db_to_data(reference_db)
                enregistrement["reference"]["text"] = enregistrement_db.reference.titre
                enregistrement["reference"]["value"] = enregistrement_db.id_reference
            return json_result(True, enregistrement=enregistrement), 200
        book_reference_db = ReferenceBibliographiqueLivre2023DB.query.filter_by(ark=ark_name).first()
        if book_reference_db:
            return json_result(True, book_reference=ReferenceBibliographiqueLivre2023.from_db_to_data(book_reference_db)), 200

        author_db = Author2023DB.query.filter_by(ark=ark_name).first()
        if author_db:
            return json_result(True, author=Author2023.from_db_to_data(author_db))

        return json_result(False), 404
    return json_result(False), 400

