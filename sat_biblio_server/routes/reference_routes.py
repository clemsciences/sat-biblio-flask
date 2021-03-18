"""
Manages book references.
Book references are here
"""

from flask import redirect, request

import logging

from data.models import ReferenceBibliographiqueLivre, Author

from sat_biblio_server import sat_biblio
from sat_biblio_server.database import db, ReferenceBibliographiqueLivreDB
from sat_biblio_server.routes import validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result
import sat_biblio_server.data.validation as dv

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region références
@sat_biblio.route("/book-references", methods=["GET", "POST"])
@validation_connexion_et_retour_defaut("email", redirect("/"), ["POST"])
def book_references():
    if request.method == "POST":
        data = request.get_json()
        if dv.check_reference_bibliographique_livre(data):
            reference_db = ReferenceBibliographiqueLivre.from_data_to_db(data)
            db.session.add(reference_db)
            db.session.commit()
            return json_result(True, message="La référence a été sauvegardée"), 201
        return json_result(False, message="La sauvegarde de la référence a échoué."), 400
    elif request.method == "GET":
        n_page = int(request.args.get("page"))
        size = int(request.args.get("size"))
        sort_by = request.args.get("sortBy")
        titre = request.args.get("titre", "")
        # print("titre", titre)

        the_query = ReferenceBibliographiqueLivreDB.query
        if titre:
            the_query = the_query.filter(ReferenceBibliographiqueLivreDB.titre.like(f"%{titre}%"))

        # sort_desc = request.args.get("sortDesc")
        # references = [{"first_name": author.first_name,
        #             "family_name": author.family_name,
        #             "id": author.id}
        #            for author in ReferenceBibliographiqueLivreDB
        #            .query.order_by(sort_by).paginate(page=n_page, per_page=size).items]
        references = []
        for reference_db in the_query.order_by(sort_by).paginate(page=n_page, per_page=size).items:
            reference = ReferenceBibliographiqueLivre.from_db_to_data(reference_db)
            reference["authors"] = " ".join(
                [f"{author['first_name']} {author['family_name']}" for author in reference['authors']])
            references.append(reference)
        logging.debug(len(references))
        return json_result(True, references=references), 200


@sat_biblio.route("/book-references/<int:id_>", methods=["GET", "PUT", "DELETE"])
@validation_connexion_et_retour_defaut("email", redirect("/"), ["PUT", "DELETE"])
def book_reference(id_):
    if request.method == "GET":
        ref_livre_db = ReferenceBibliographiqueLivre.from_id_to_db(id_)
        if ref_livre_db:
            ref_livre = ReferenceBibliographiqueLivre.from_db_to_data(ref_livre_db)

            ref_livre["authors"] = [{"text": f"{author_db.first_name} {author_db.family_name}", "value": author_db.id}
                                    for author_db in ref_livre_db.authors]
            logging.debug(ref_livre)
            return json_result(True, reference=ref_livre), 200
        return json_result(False), 404
    elif request.method == "PUT":
        data = request.get_json()
        ref_biblio_db = ReferenceBibliographiqueLivre.from_id_to_db(id_)
        if ref_biblio_db:
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

            return json_result(True), 200
        return json_result(False), 404
    elif request.method == "DELETE":
        ref_biblio_db = ReferenceBibliographiqueLivreDB.query.filter_by(id=id_).first()
        if ref_biblio_db:
            db.session.delete(ref_biblio_db)
            db.session.commit()
            return json_result(True), 204
        return json_result(False), 404


@sat_biblio.route("/book-references/count", methods=["GET"])
def book_references_count():
    titre = request.args.get("titre", "")
    the_query = ReferenceBibliographiqueLivreDB.query
    if titre:
        the_query = the_query.filter(ReferenceBibliographiqueLivreDB.titre.like(f"%{titre}%"))
    count = the_query.count()
    logging.debug(count)
    return json_result(True, total=count), 200


@sat_biblio.route("/book-references/chercher-proches", methods=["GET"])
def chercher_reference_livre_plus_proches():
    titre = request.args.get("titre")
    references_db = ReferenceBibliographiqueLivreDB.query\
        .filter(ReferenceBibliographiqueLivreDB.titre.like(f"%{titre}%")).all()
    references = []
    for reference_db in references_db:
        # reference = ReferenceBibliographiqueLivre.from_db_to_data(reference_db)
        references.append({"text": reference_db.titre,
                           "value": reference_db.id})
    return json_result(True, suggestedReferences=references), 200


@sat_biblio.route("/book-references/chercher", methods=["POST"])
def chercher_reference_livre():
    data = request.get_json()
    the_query = ReferenceBibliographiqueLivreDB.query
    if "titre" in data and data["titre"]:
        the_query = the_query.filter(ReferenceBibliographiqueLivreDB.titre.like(f"%{data['titre']}%"))
        ref_livres_db = the_query.all()
        results = [ReferenceBibliographiqueLivre.from_db_to_data(ref_livre_db)
                   for ref_livre_db in ref_livres_db]
        return json_result(True, results=results)
    return json_result(True, results=[]), 200
# endregion
