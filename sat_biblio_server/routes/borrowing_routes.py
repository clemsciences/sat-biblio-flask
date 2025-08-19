"""

"""

import datetime
import json

from flask import redirect, session, request

import logging

from managers.log_manager import LogEventManager
from sat_biblio_server.data.models import EmpruntLivre
from sat_biblio_server.managers.mail_manager import send_new_borrowing_email
from sat_biblio_server.sessions import UserSess

from sat_biblio_server import sat_biblio, UserDB, EmpruntLivre2023DB, ReferenceBibliographiqueLivre2023DB, \
    Enregistrement2023DB
from sat_biblio_server.database import db
from sat_biblio_server.data.models_2023 import EmpruntLivre
from sat_biblio_server.routes import get_pagination, validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result
import sat_biblio_server.data.validation as dv
from sqlalchemy import or_

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region borrowing
@sat_biblio.route("/borrowings/", methods=["POST", "GET"])
@validation_connexion_et_retour_defaut("email", ["DELETE", "PUT"])
def borrowings():
    if request.method == "GET":
        n_page, size, sort_by = get_pagination(request)
        borrowing_date_before_today = request.args.get("borrowing-date-before-today", None)
        query = EmpruntLivre2023DB.query

        id_emprunteur = request.args.get("id_emprunteur", -1)
        if id_emprunteur > 0:
            query = query.filter(EmpruntLivre2023DB.id_emprunteur == id_emprunteur)

        id_enregistrement = request.args.get("id_enregistrement", -1)
        if id_enregistrement > 0:
            query = query.filter(EmpruntLivre2023DB.id_enregistrement == id_enregistrement)

        id_gestionnaire = request.args.get("id_gestionnaire", -1)
        if id_gestionnaire > 0:
            query = query.filter(EmpruntLivre2023DB.id_enregistrement == id_gestionnaire)

        commentaire = request.args.get("commentaire")
        if commentaire:
            query = query.filter(EmpruntLivre2023DB.commentaire.like(commentaire))

        in_commentaire = request.args.get("in_commentaire")
        if in_commentaire:
            query = query.filter(EmpruntLivre2023DB.commentaire.like(f"%{commentaire}%"))

        emprunte = request.args.get("emprunte")
        if emprunte:
            query = query.filter(EmpruntLivre2023DB.emprunte == emprunte)

        # date_emprunt = request.args.get("date_emprunt")
        # if date_emprunt:
        #     query = query.filter(EmpruntLivreDB.date_emprunt == date_emprunt)
        #
        # date_retour_prevu = request.args.get("date_retour_prevu")
        # if date_retour_prevu:
        #     query = query.filter(EmpruntLivreDB.date_retour_prevu == date_retour_prevu)
        #
        # date_retour_reel = request.args.get("date_retour_reel")
        # if date_retour_reel:
        #     query = query.filter(EmpruntLivreDB.date_retour_reel == date_retour_reel)

        on_time = request.args.get("on_time")
        late = request.args.get("late")
        all_about_late = request.args.get("all")
        if all_about_late == "all":
            pass
        elif on_time == "true":
            query = query.filter(
                or_(EmpruntLivre2023DB.date_retour_prevu > datetime.date.today(),
                    EmpruntLivre2023DB.rendu == True))
        elif late == "true":
            query = query.filter(EmpruntLivre2023DB.date_retour_prevu <= datetime.date.today())

        rendu = request.args.get("rendu")
        if rendu:
            if rendu == "true":
                rendu = True
            else:
                rendu = False
            query = query.filter(EmpruntLivre2023DB.rendu == rendu)
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
        # logging.log(logging.DEBUG, data)
        if dv.check_emprunt(data):
            current_user_db = UserDB.query.filter_by(email=session["email"]).first()
            borrower_db = UserDB.query.filter_by(id=data["borrower"]).first()
            if borrower_db:
                date_retour_prevu = datetime.date.fromisoformat(data["dateComebackExpected"])
                record_db = Enregistrement2023DB.query.filter_by(id=data["record"]).first()
                if record_db:
                    existing_record_borrowing = EmpruntLivre2023DB.query.filter_by(id_enregistrement=record_db.id).first()
                    if existing_record_borrowing:
                        return json_result(False, "L'ouvrage demandé est déjà emprunté.")
                    reference_db = (ReferenceBibliographiqueLivre2023DB
                                 .query
                                 .filter_by(id=record_db.id)
                                 .first())
                    borrowing_db = EmpruntLivre2023DB(id_emprunteur=data["borrower"],
                                                 id_enregistrement=data["record"],
                                                 id_gestionnaire=current_user_db.id,
                                                 commentaire=data["comment"],
                                                 date_retour_prevu=date_retour_prevu,  # TODO string to date
                                                 emprunte=True,
                                                 rendu=False)
                    borrowing_db.enregistrement = record_db
                    db.session.add(borrowing_db)
                    db.session.commit()
                    LogEventManager(db).add_create_event(borrowing_db.id, session.get("id", -1),
                                                         EmpruntLivre2023DB.__tablename__,
                                                         values=json.dumps(EmpruntLivre.from_db_to_data(borrowing_db)))

                    success = send_new_borrowing_email(borrower_db, reference_db, borrowing_db)
                    if success:
                        return json_result(True, "L'enregistrement de la fiche d'emprunt et l'envoi de l'email se sont correctement passé.", id=borrowing_db.id), 201
                    return json_result(False, id=borrowing_db.id, message="Echec de l'envoi de l'email d'emprunt."), 200
                return json_result(False, "L'enregistrmeent n'est pas reconnu. Contactez l'administrateur.")
            else:
                return json_result(False, "L'emprunteur n'est pas reconnu. Contactez l'administrateur.")
        return json_result(False, message="Wrong data type"), 400
    return json_result(False), 400


@sat_biblio.route("/borrowings/<int:id_>/", methods=["GET", "DELETE", "PUT"])
@validation_connexion_et_retour_defaut("email", ["DELETE", "PUT"])
def borrowing(id_: int):
    """

    :return:
    """
    if request.method == "GET":
        borrowing_db = EmpruntLivre2023DB.query.filter_by(id=id_).first()
        if borrowing_db:
            borrowing_data = EmpruntLivre.from_db_to_data(borrowing_db)
            return json_result(True, borrowing=borrowing_data), 200
        else:
            return json_result(False), 404

    elif request.method == "DELETE":
        borrowing_db = EmpruntLivre2023DB.query.filter_by(id=id_).first()
        if borrowing_db:
            db.session.delete(borrowing_db)
            db.session.commit()
            LogEventManager(db).add_delete_event(borrowing_db.id, session.get("id", -1),
                                                 EmpruntLivre2023DB.__tablename__,
                                                 values=json.dumps(EmpruntLivre.from_db_to_data(borrowing_db)))
            return json_result(True), 204
        else:
            return json_result(True), 404

    elif request.method == "PUT":
        data = request.get_json()
        if "borrowing" in data:
            borrowing_data = data["borrowing"]
            # borrowing_db_from_request = EmpruntLivre.from_data_to_db(borrowing_data)

            borrowing_db = EmpruntLivre2023DB.query.filter_by(id=id_).first()
            if borrowing_db:
                id_emprunteur = borrowing_data.get("id_emprunteur", -1)
                if id_emprunteur > 0:
                    borrowing_db.id_emprunteur = id_emprunteur

                id_enregistrement = borrowing_data.get("id_enregistrement", -1)
                if id_enregistrement > 0:
                    borrowing_db.id_enregistrement = id_enregistrement

                id_gestionnaire = borrowing_data.get("id_gestionnaire", -1)
                if id_gestionnaire > 0:
                    borrowing_db.id_gestionnaire = id_gestionnaire

                if "commentaire" in borrowing_data:
                    borrowing_db.commentaire = borrowing_data["commentaire"]

                if "emprunte" in borrowing_data:
                    borrowing_db.emprunte = borrowing_data["emprunte"]

                if "date_emprunt" in borrowing_data:
                    try:
                        borrowing_db.date_emprunt = datetime.date.fromisoformat(borrowing_data["date_emprunt"])  # borrowing_data["date_emprunt"]
                    except ValueError:
                        borrowing_db.date_emprunt = None

                if "date_retour_prevu" in borrowing_data:
                    try:
                        borrowing_db.date_retour_prevu = datetime.date.fromisoformat(borrowing_data["date_retour_prevu"])
                    except ValueError:
                        borrowing_db.date_retour_prevu = None

                if "date_retour_reel" in borrowing_data:
                    try:
                        borrowing_db.date_retour_reel = datetime.date.fromisoformat(borrowing_data["date_retour_reel"])
                    except ValueError:
                        borrowing_db.date_retour_reel = None

                if "rendu" in borrowing_data:
                    borrowing_db.rendu = borrowing_data["rendu"]

                db.session.commit()
                borrowing_data = EmpruntLivre.from_db_to_data(borrowing_db)
                LogEventManager(db).add_delete_event(borrowing_db.id, session.get("id", -1),
                                                     EmpruntLivre2023DB.__tablename__,
                                                     values=json.dumps(borrowing_data))
                return json_result(True, borrowing=borrowing_data,
                                   message="La fiche de l'emprunt vient d'être mise à jour."), 200
            else:
                return json_result(False, "Erreur lors de la récupération de la fiche de l'emprunt."), 404
        return json_result(False, "Echec de la mise à jour de la fiche de l'emprunt."), 400


@sat_biblio.route("/borrowings/count/", methods=["GET"])
def borrowings_count():
    """

    :return:
    """
    the_query = EmpruntLivre2023DB.query
    the_total_query = EmpruntLivre2023DB.query

    id_emprunteur = request.args.get("id_emprunteur", -1)
    if id_emprunteur > 0:
        the_query = the_query.filter(EmpruntLivre2023DB.id_emprunteur == id_emprunteur)

    id_enregistrement = request.args.get("id_enregistrement", -1)
    if id_enregistrement > 0:
        the_query = the_query.filter(EmpruntLivre2023DB.id_enregistrement == id_enregistrement)

    id_gestionnaire = request.args.get("id_gestionnaire", -1)
    if id_gestionnaire > 0:
        the_query = the_query.filter(EmpruntLivre2023DB.id_enregistrement == id_gestionnaire)

    commentaire = request.args.get("commentaire")
    if commentaire:
        the_query = the_query.filter(EmpruntLivre2023DB.commentaire.like(commentaire))

    in_commantaire = request.args.get("in_commentaire")
    if in_commantaire:
        the_query = the_query.filter(EmpruntLivre2023DB.commentaire.like(f"%{commentaire}%"))

    emprunte = request.args.get("emprunte")
    if emprunte:
        the_query = the_query.filter(EmpruntLivre2023DB.emprunte == emprunte)

    date_emprunt = request.args.get("date_emprunt")
    if date_emprunt:
        the_query = the_query.filter(EmpruntLivre2023DB.date_emprunt == date_emprunt)

    date_retour_prevu = request.args.get("date_retour_prevu")
    if date_retour_prevu:
        the_query = the_query.filter(EmpruntLivre2023DB.date_retour_prevu == date_retour_prevu)

    date_retour_reel = request.args.get("date_retour_reel")
    if date_retour_reel:
        the_query = the_query.filter(EmpruntLivre2023DB.date_retour_reel == date_retour_reel)

    on_time = request.args.get("on_time")
    late = request.args.get("late")
    _all_about_late = request.args.get("all")
    if _all_about_late == "true":
        pass
    elif on_time == "true":
        the_query = the_query.filter(
            or_(EmpruntLivre2023DB.date_retour_prevu > datetime.date.today(),
                EmpruntLivre2023DB.rendu == True))
    elif late == "true":
        the_query = the_query.filter(EmpruntLivre2023DB.date_retour_prevu <= datetime.date.today())

    rendu = request.args.get("rendu")
    if rendu:
        if rendu == "true":
            rendu = True
        else:
            rendu = False
        the_query = the_query.filter(EmpruntLivre2023DB.rendu == rendu)

    filtered_count = the_query.count()
    total_count = the_total_query.count()

    # borrowing_db.id_emprunteur =

    return json_result(True, total=total_count, filtered_number=filtered_count), 200
# endregion
