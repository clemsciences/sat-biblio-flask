"""

"""
import codecs
import csv
import os
import time

from flask import request, session, send_file

from sat_biblio_server.data.models import Enregistrement
from sat_biblio_server import sat_biblio, UserDB, json_result, EnregistrementDB, PACKDIR


@sat_biblio.route("/export/csv/", methods=["GET"])
def export_catalogue():
    """

    :return:
    """

    records_db = EnregistrementDB.query.all()
    records = [Enregistrement.from_db_to_data(record_db) for record_db in records_db]
    filename = f"catalogue-{time.time()}.csv"
    print(os.getcwd())
    with codecs.open(os.path.join(PACKDIR, "static", filename), "w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["Auteurs", "Titre", "Lieu d'édition", "Editeur", "Année", "Nombre de pages",
                         "Année d'obtention", "Description", "Commentaire", "Cote",
                         "Nombre d'exemplaire supplémentaire", "Provenance", "Mots-clés"])
        for record in records:
            # print(record)
            writer.writerow(Enregistrement.from_data_to_csv_row(record))
    return send_file(os.path.join("static", filename))  # json_result(True, records=records)


