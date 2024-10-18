import os

from flask import request
from sqlalchemy.orm import Session

from sat_biblio_referencement import TABLE_PUBLICATION_2004_FILENAME
from sat_biblio_referencement.database.database_manager import DatabaseManager
from sat_biblio_referencement.data.search_manager import SearchManager
from sat_biblio_referencement.scripts.populate_table_publication_2004 import generate_publication_table_2004

from sat_biblio_server import PACKDIR, sat_biblio, json_result

TABLE_PUBLICATION_2004_PATH = os.path.join(PACKDIR, "static", TABLE_PUBLICATION_2004_FILENAME)
sbr_dbm = DatabaseManager(False, False, path=TABLE_PUBLICATION_2004_PATH)
sbr_dbm.prepare()


@sat_biblio.route("/search/works/", methods=["GET"])
def search_works_route():
    # is_approximate = request.args.get("approximate", "false") == "true"
    query = request.args.get("query")
    session = Session(sbr_dbm.engine)
    suggestions = SearchManager.get_data_from_query(session, query)
    session.close()
    return json_result(True, suggestions=suggestions), 200


@sat_biblio.route("/search/populate-publication-table-2004/", methods=["GET"])
def populate_publication_table_2004_request():
    generate_publication_table_2004(TABLE_PUBLICATION_2004_PATH)
    return json_result(True)


@sat_biblio.route("/search/named-entities/", methods=["GET"])
def search_named_entities():
    query = request.args.get("query")
    session = Session(sbr_dbm.engine)
    near_named_entities = SearchManager.search_near_named_entities(session, query)
    session.close()
    return json_result(True, suggestions=near_named_entities)
