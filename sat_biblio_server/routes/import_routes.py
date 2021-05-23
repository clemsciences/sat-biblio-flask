import codecs
import csv
import os

from flask import request

from sat_biblio_server import sat_biblio, json_result, PACKDIR
import sat_biblio_server.data.import_csv_utils as icu

SCRIPT_PATH = os.path.join(PACKDIR, "scripts", "inven.csv")
rows = []
i = 0
with codecs.open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    for row in csv.reader(f, delimiter=";"):
        if i > 0:
            description = row[0]
            rows.append({"description": description,
                         "cote": row[1],
                         "nb_supp": row[2],
                         "annee": row[3],
                         "provenance": row[4],
                         "theme1": row[5],
                         "theme2": row[6],
                         "theme3": row[7],
                         "index": i})
        i += 1


@sat_biblio.route("/import-csv/")
def import_csv():
    n_page = int(request.args.get("page"))
    size = int(request.args.get("size"))
    print(n_page, size)
    return json_result(True, rows=rows[(n_page - 1) * size:n_page * size]), 200


@sat_biblio.route("/import-csv/count/")
def get_import_csv_count():
    print("count")
    return json_result(True, total=len(rows)), 200


@sat_biblio.route("/import-csv/rows/<int:n_row>")
def process_row(n_row):
    processed_row = rows[n_row-1]
    print(processed_row)
    description = processed_row["description"]
    print(description)
    # auteur = description.split(",")
    # print(auteur[0])
    # reste = "".join(auteur[1:])
    # print(reste)
    # authors = icu.extraire_auteurs(auteur)
    ref = icu.extraire_ref_biblio(description)
    # return json_result(True, data=processed_row, ref=ref, authors=authors), 200
    return json_result(True, data=processed_row, ref=ref), 200
