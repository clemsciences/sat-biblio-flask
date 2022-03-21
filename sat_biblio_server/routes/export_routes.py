"""

"""

from flask import request, session, send_file

from data.models import Enregistrement
from sat_biblio_server import sat_biblio, UserDB, json_result, EnregistrementDB


@sat_biblio.route("/export/csv/", methods=["GET"])
def export_catalogue():
    """

    :return:
    """

    records = EnregistrementDB.query.all()
    [Enregistrement.from_db_to_data(record_db) for record_db in records]

