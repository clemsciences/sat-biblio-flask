import codecs
import csv
import os
import pickle

from flask import request

from data.models import Author, ReferenceBibliographiqueLivre, Enregistrement
from sat_biblio_server import sat_biblio, json_result, PACKDIR, app, AuthorDB, db
import sat_biblio_server.data.import_csv.import_csv_utils as icu


INVENTORY_PATH = os.path.join(PACKDIR, "scripts", "inventaire-21-07-23.csv")

# region
ALREADY_STORED_ROW_PATH = os.path.join(PACKDIR, "scripts", "already_stored_row.pickle")


def get_already_stored_rows():
    if os.path.exists(ALREADY_STORED_ROW_PATH):
        with open(ALREADY_STORED_ROW_PATH, "rb") as f:
            return pickle.load(f)
    return set()


def store_new_stored_row(new_row):
    already_stored_rows.add(new_row)
    with open(ALREADY_STORED_ROW_PATH, "wb") as f:
        pickle.dump(already_stored_rows, f)


def remove_row_from_stored(n_row):
    if n_row in already_stored_rows:
        already_stored_rows.remove(n_row)
    with open(ALREADY_STORED_ROW_PATH, "wb") as f:
        pickle.dump(already_stored_rows, f)


def get_next_not_marked_row(n_row):
    sorted_rows = sorted(list(already_stored_rows))
    if n_row == 0:
        n_row += 1
    if n_row in sorted_rows:
        index_row = sorted_rows.index(n_row)
        for j in range(index_row+1, len(rows)):
            if j not in sorted_rows:
                return j
    return -1


already_stored_rows = get_already_stored_rows()

# endregion


rows = []
if os.path.exists(INVENTORY_PATH):
    i = 0
    with codecs.open(INVENTORY_PATH, "r", encoding="windows-1252") as f:
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


@sat_biblio.route("/import-csv/rows/<int:n_row>/add-store", methods=["GET", "POST"])
def add_to_store(n_row):
    store_new_stored_row(n_row)
    return json_result(True), 200


@sat_biblio.route("/import-csv/rows/<int:n_row>/remove-store", methods=["GET", "POST"])
def remove_from_store(n_row):
    remove_row_from_stored(n_row)
    return json_result(True, message="pas bon"), 200


@sat_biblio.route("/import-csv/rows/<int:n_row>/go-to-next-not-marked-row")
def go_to_next_not_marked_row(n_row):
    n = get_next_not_marked_row(n_row)
    return json_result(True, n=n), 200


@sat_biblio.route("/import-csv/rows/<int:n_row>", methods=["GET", "POST"])
def load_row(n_row):
    processed_row = rows[n_row]
    print(processed_row)
    description = processed_row["description"]
    print(description)
    if request.method == "GET":
        ref = icu.extraire_ref_biblio(description)
        record = icu.extraire_enregistrements(processed_row)
        already_stored = n_row in already_stored_rows
        return json_result(True, data=processed_row, ref=ref, record=record, already_stored=already_stored), 200
    elif request.method == "POST":
        store_new_stored_row(n_row)
        return json_result(True), 200
    return json_result(True, message="pas bon"), 400


# @sat_biblio.route("/import-csv/all")
# def import_all():
#     for row in rows:
#         description = row["description"]
#         ref = icu.extraire_ref_biblio(description)
#         authors = ref["authors"]
#         Author.from_data_to_db()
#
#         record = icu.extraire_enregistrements(row)
#         author_db = Author.from_data_to_db(data)
#
#         db.session.add(author_db)
#         db.session.commit()


@sat_biblio.route("/import/", methods=["GET", "POST"])
def import_catalogue_from_file():
    print(app.config)

    # if request.method == "POST":
    #     if "file" in request.files:
    #         file = request.files["file"]
    #         filename = secure_filename(file.filename)
    #         sat_biblio.config
    #         file.save()


@sat_biblio.route("/import/all/", methods=["GET", "POST"])
def import_complete_catalogue_from_file():
    for number, processed_row in enumerate(rows[1:]):
        if number % 10 == 0:
            print(number)
        # print(processed_row)
        description = processed_row["description"]
        # print(description)
        ref = icu.extraire_ref_biblio(description)
        if ref is None:
            print(number, "ref is None")
            continue
        if "authors" not in ref:
            print(number, "failed because authors not in ref")
            continue
        auteurs = []
        for author in ref["authors"]:
            # print(author)
            author_exists = AuthorDB.query.filter_by(first_name=author["first_name"],
                                                     family_name=author["family_name"]).first()
            if not author_exists:
                author_db = Author.from_data_to_db(author)
                db.session.add(author_db)
                db.session.commit()
                author_exists = author_db
            auteurs.append(dict(value=author_exists.id))
        # if dv.check_reference_bibliographique_livre(ref):
        ref["auteurs"] = auteurs
        # print(ref)
        reference_db = ReferenceBibliographiqueLivre.from_data_to_db(ref)
        # print(reference_db)
        db.session.add(reference_db)
        db.session.commit()
        record = icu.extraire_enregistrements(processed_row)
        if record is None:
            print("record is None")
            continue
        # print(record)
        enregistrement_db = Enregistrement.from_data_to_db(record)
        # print(enregistrement_db)
        db.session.add(enregistrement_db)
        db.session.commit()
        # store_new_stored_row(processed_row)
        # return json_result(True, data=processed_row, ref=ref, record=record, already_stored=already_stored), 200
    return json_result(True), 200
