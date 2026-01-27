"""
Manages records in library.

Records are hints to manage books in the library.
"""
import datetime
import logging
import re

from flask import redirect, request

from sat_biblio_server import sat_biblio, LogEventDB, UserDB
from sat_biblio_server.data.models import LogEvent
import sat_biblio_server.data.validation as dv
from sat_biblio_server.database import db
from sat_biblio_server.routes import get_pagination, int_to_bool, validation_connexion_et_retour_defaut
from sat_biblio_server.utils import json_result

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region log events
@sat_biblio.route("/log-events/", methods=["GET", "POST"])
@validation_connexion_et_retour_defaut("email", ["POST", "PUT"])
def log_events_request():
    if request.method == "POST":
        data = request.get_json()
        if dv.check_log_event(data):
            log_event_db = LogEvent.from_data_to_db(data)
            db.session.add(log_event_db)
            db.session.commit()
            return json_result(True, id=log_event_db.id, message="Log event."), 201
        return json_result(False, message="Erreur de la sauvegarde de l'événement."), 400
    elif request.method == "GET":
        n_page, size, sort_by, sort_desc = get_pagination(request)

        # region filtre
        from_datetime_str = request.args.get("from_datetime", None)
        to_datetime_str = request.args.get("to_datetime", None)
        table_name = request.args.get("tablename", "")

        the_query = LogEventDB.query
        if from_datetime_str:
            from_datetime = datetime.datetime.fromisoformat(from_datetime_str)
            the_query = the_query.filter(LogEventDB.event_datetime >= from_datetime)
        if to_datetime_str:
            to_datetime = datetime.datetime.fromisoformat(to_datetime_str)
            the_query = the_query.filter(LogEventDB.event_datetime <= to_datetime)
        if table_name:
            the_query = the_query.filter(LogEventDB.table_name.like(f"%{table_name}%"))
        # endregion

        if sort_by:
            the_query = the_query.order_by(sort_by)
        else:
            the_query = the_query.order_by("event_datetime")

        log_events = []
        for log_event_db in the_query.paginate(page=n_page, per_page=size).items:
            log_event = LogEvent.from_db_to_data(log_event_db)
            event_owner_user = UserDB.query.filter_by(id=log_event_db.event_owner_id).first()
            if event_owner_user:
                log_event["event_owner"] = event_owner_user.pretty_string()
            else:
                log_event["event_owner"] = "Unknown"
            # print(record)
            log_events.append(log_event)
        return json_result(True, log_events=log_events), 200


@sat_biblio.route("/log-events/<int:id_>/", methods=["GET", "DELETE", "PUT"])
@validation_connexion_et_retour_defaut("email", ["DELETE", "PUT"])
def log_event_request(id_):
    if request.method == "GET":
        log_event_db = LogEventDB.query.filter_by(id=id_).first()
        if log_event_db:
            log_event = LogEvent.from_db_to_data(log_event_db)
            return json_result(True, log_event=log_event), 200
        return json_result(False), 404
    elif request.method == "DELETE":
        log_event_db = LogEventDB.query.filter_by(id=id_).first()
        if log_event_db:
            db.session.delete(log_event_db)
            db.session.commit()
            return json_result(True), 204
        else:
            return json_result(False), 404
    elif request.method == "PUT":
        data = request.get_json()
        log_event_db = LogEventDB.query.filter_by(id=id_).first()
        if log_event_db:
            if "id" in data:
                log_event_db.id = data["id"]
            if "event_type" in data:
                log_event_db.event_type = data["event_type"]
            if "object_id" in data:
                log_event_db.cote = data["object_id"]
            if "event_datetime" in data:
                log_event_db.event_datetime = datetime.datetime.fromisoformat(data["event_datetime"])
            if "event_owner_id" in data:
                log_event_db.event_owner_id = data["event_owner_id"]
            if "table_name" in data:
                log_event_db.table_name = data["table_name"]
            db.session.commit()
            return json_result(True, "Evenement correctement mis à jour."), 200
        return json_result(False, "Echec de la mise à jour de l'événement."), 404


@sat_biblio.route("/log-events/count/", methods=["GET"])
def log_events_count():
    table_name = request.args.get("table_name", "")
    event_owner_id = request.args.get("event_owner_id", "")
    object_id = request.args.get("object_id", "")
    from_event_datetime_str = request.args.get("from_event_datetime", "")
    to_event_datetime_str = request.args.get("to_event_datetime", "")

    the_query = LogEventDB.query
    if table_name:
        the_query = the_query.filter(LogEventDB.table_name.like(f"%{table_name}%"))
    if event_owner_id:
        the_query = the_query.filter_by(event_owner_id=event_owner_id)
    if object_id:
        the_query = the_query.filter_by(object_id=object_id)
    if from_event_datetime_str:
        from_event_datetime = datetime.datetime.fromisoformat(from_event_datetime_str)
        the_query = the_query.filter(LogEventDB.event_datetime >= from_event_datetime)
    if to_event_datetime_str:
        to_event_datetime = datetime.datetime.fromisoformat(to_event_datetime_str)
        the_query = the_query.filter(LogEventDB.event_datetime <= to_event_datetime)

    number = the_query.count()
    logging.debug(number)
    return json_result(True, total=number), 200
# endregion
