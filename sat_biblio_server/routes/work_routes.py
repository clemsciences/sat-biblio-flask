import os
from flask import request
from sqlalchemy.orm import Session

from sat_biblio_referencement import TABLE_PUBLICATION_2004_FILENAME
from sat_biblio_referencement.database.database_manager import DatabaseManager
from sat_biblio_referencement.database import PublishedWorksDB
from sat_biblio_referencement.data.published_work_data import PublishedWorksData

from sat_biblio_server import json_result, sat_biblio, PACKDIR

TABLE_PUBLICATION_2004_PATH = os.path.join(PACKDIR, "static", TABLE_PUBLICATION_2004_FILENAME)
sbr_dbm = DatabaseManager(False, False, path=TABLE_PUBLICATION_2004_PATH)
sbr_dbm.prepare()


@sat_biblio.route("/works/published/", methods=["GET", "POST"])
def published_works_list_request():
    """
    published_works
    :return:
    """
    if request.method == "GET":

        session = Session(sbr_dbm.engine)
        published_works_db = session.query(PublishedWorksDB).all()
        published_works = [PublishedWorksData.from_db_to_data(i) for i in published_works_db]
        session.close()
        return json_result(True, result=published_works), 200
    elif request.method == "POST":
        session = Session(sbr_dbm.engine)
        data = request.get_json()
        PublishedWorksData.from_data_to_db(data)
        session.add(data)
        session.commit()
        session.close()
        return json_result(True, "Ajout d'une oeuvre publiée correctement effectué."), 200
    return json_result(False), 304


@sat_biblio.route("/works/published/<int:id_>/", methods=["GET", "PUT", "DELETE"])
def published_work_request(id_):
    """
    published_works

    :param id_:
    :return:
    """
    if request.method == "GET":
        session = Session(sbr_dbm.engine)
        published_work_db = session.query(PublishedWorksDB).filter_by(id_=id_).first()
        published_work = PublishedWorksData.from_db_to_data(published_work_db)
        session.commit()
        session.close()
        return json_result(True, result=published_work), 200
    elif request.method == "PUT":
        data = request.get_json()
        published_word_db_from_data = PublishedWorksData.from_data_to_db(data)
        session = Session(sbr_dbm.engine)
        published_word_db = session.query(PublishedWorksDB).filter_by(id_=id_).first()
        published_word_db.title = published_word_db_from_data.title
        published_word_db.year = published_word_db_from_data.year
        published_word_db.publication_type = published_word_db_from_data.publication_type
        session.commit()
        session.close()
        return json_result(True, "Enregistrement de la mise à jour de l'oeuvre publiée.")
    return json_result(False, "Echec de la requête."), 304
