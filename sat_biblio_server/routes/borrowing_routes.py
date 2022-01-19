"""

"""

import datetime
from flask import redirect, session, request

import logging

from sat_biblio_server.data.models import EmpruntLivre
from sat_biblio_server.sessions import UserSess

from sat_biblio_server.database import db, EmpruntLivreDB
from sat_biblio_server import sat_biblio
from sat_biblio_server.routes import get_pagination, validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result
import sat_biblio_server.data.validation as dv

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region borrowing
@sat_biblio.route("/borrowings/", methods=["POST", "GET"])
@validation_connexion_et_retour_defaut("email", ["DELETE", "PUT"])
def borrowings():
    if request.method == "GET":
        n_page, size, sort_by = get_pagination(request)
        borrowing_date_before_today = request.args.get("borrowing-date-before-today", None)
        query = EmpruntLivreDB.query
        if borrowing_date_before_today:
            borrowing_date_before_today = int(borrowing_date_before_today)
            date = datetime.date.fromtimestamp(borrowing_date_before_today)
            logging.warning(borrowing_date_before_today)
            query = query.filter_by(date_retour_prevu=date)
        if sort_by:
            query = query.order_by(sort_by)
        query = query.paginate(page=n_page, per_page=size)
        borrowings_db = query.items
        borrowings_data = [EmpruntLivre.from_db_to_data(borrowing_db) for borrowing_db in borrowings_db]
        return json_result(True, borrowings=borrowings_data), 200
    elif request.method == "POST":
        data = request.get_json()
        logging.log(logging.DEBUG, data)
        if dv.check_emprunt(data):
            user = UserSess(session["email"])
            emprunt = EmpruntLivreDB(id_emprunteur=data["borrower"]["value"],
                                     id_enregistrement=data["record"],
                                     id_gestionnaire=user.user_db.id,
                                     commentaire=data["comment"],
                                     emprunte=True,
                                     rendu=False)
            db.session.add(emprunt)
            db.session.commit()
            return json_result(True, id=emprunt.id), 201
        return json_result(False, message="Wrong data type"), 400
    return json_result(False), 400


@sat_biblio.route("/borrowings/<int:id_>/", methods=["GET", "DELETE", "PUT"])
@validation_connexion_et_retour_defaut("email", ["DELETE", "PUT"])
def borrowing(id_: int):
    """

    :return:
    """
    if request.method == "GET":
        borrowing_db = EmpruntLivreDB.query.filter_by(id=id_).first()
        if borrowing_db:
            borrowing_data = EmpruntLivre.from_db_to_data(borrowing_db)
            return json_result(True, borrowing=borrowing_data), 200
        else:
            return json_result(False), 404

    elif request.method == "DELETE":
        borrowing_db = EmpruntLivreDB.query.filter_by(id=id_).first()
        if borrowing_db:
            db.session.delete(borrowing_db)
            db.session.commit()
            return json_result(True), 204
        else:
            return json_result(True), 404

    elif request.method == "PUT":
        data = request.get_json()
        borrowing_data = None
        if "borrowing" in data:
            borrowing_data = data["borrowing"]
            borrowing_db_from_request = EmpruntLivre.from_data_to_db(borrowing_data)

            borrowing_db = EmpruntLivreDB.query.filter_by(id=id_).first()
            if borrowing_db:

                id_emprunteur = borrowing_data.get("id_emprunteur", -1)
                if id_emprunteur < 0:
                    borrowing_db.id_emprunteur = id_emprunteur

                id_enregistrement = borrowing_data.get("id_enregistrement", -1)
                if id_enregistrement < 0:
                    borrowing_db.id_enregistrement = id_enregistrement

                id_gestionnaire = borrowing_data.get("id_gestionnaire", -1)
                if id_gestionnaire < 0:
                    borrowing_db.id_gestionnaire = id_gestionnaire

                if "commentaire" in borrowing_data:
                    borrowing_db.commentaire = borrowing_data["commentaire"]

                if "emprunte" in borrowing_data:
                    borrowing_db.emprunte = borrowing_data["emprunte"]

                if "date_emprunt" in borrowing_data:
                    borrowing_db.date_emprunt = borrowing_db_from_request.date_emprunt  # borrowing_data["date_emprunt"]

                if "date_retour_prevu" in borrowing_data:
                    borrowing_db.date_retour_prevu = borrowing_db_from_request.date_retour_prevu

                if "date_retour_reel" in borrowing_data:
                    borrowing_db.date_retour_reel = borrowing_db_from_request.date_retour_reel

                if "rendu" in borrowing_data:
                    borrowing_db.rendu = borrowing_db_from_request.rendu

                db.session.commit()
                borrowing_data = EmpruntLivre.from_db_to_data(borrowing_db)
                return json_result(True, borrowing=borrowing_data), 200
            else:
                return json_result(False), 404
        return json_result(False), 400


@sat_biblio.route("/borrowings/count/", methods=["GET"])
def borrowings_count():
    """

    :return:
    """
    the_query = EmpruntLivreDB.query

    id_emprunteur = request.args.get("id_emprunteur", -1)
    if id_emprunteur < 0:
        the_query = the_query.filter(EmpruntLivreDB.id_emprunteur == id_emprunteur)

    id_enregistrement = request.args.get("id_enregistrement", -1)
    if id_enregistrement < 0:
        the_query = the_query.filter(EmpruntLivreDB.id_enregistrement == id_enregistrement)

    id_gestionnaire = request.args.get("id_gestionnaire", -1)
    if id_gestionnaire < 0:
        the_query = the_query.filter(EmpruntLivreDB.id_enregistrement == id_gestionnaire)

    commentaire = request.args.get("commentaire")
    if commentaire:
        the_query = the_query.filter(EmpruntLivreDB.commentaire.like(commentaire))

    in_commantaire = request.args.get("in_commentaire")
    if in_commantaire:
        the_query = the_query.filter(EmpruntLivreDB.commentaire.like(f"%{commentaire}%"))

    emprunte = request.args.get("emprunte")
    if emprunte:
        the_query = the_query.filter(EmpruntLivreDB.emprunte == emprunte)

    date_emprunt = request.args.get("date_emprunt")
    if date_emprunt:
        the_query = the_query.filter(EmpruntLivreDB.date_emprunt == date_emprunt)

    date_retour_prevu = request.args.get("date_retour_prevu")
    if date_retour_prevu:
        the_query = the_query.filter(EmpruntLivreDB.date_retour_prevu == date_retour_prevu)

    date_retour_reel = request.args.get("date_retour_reel")
    if date_retour_reel:
        the_query = the_query.filter(EmpruntLivreDB.date_retour_reel == date_retour_reel)

    rendu = request.args.get("rendu")
    if rendu:
        if rendu == "true":
            rendu = True
        else:
            rendu = False
        the_query = the_query.filter(EmpruntLivreDB.rendu == rendu)

    total = the_query.count()

    # borrowing_db.id_emprunteur =

    return json_result(True, total=total), 200
# endregion
