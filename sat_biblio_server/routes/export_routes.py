"""

"""
import datetime
import logging
import os

from sat_biblio_server.managers.export_manager import ExportCatalogueManager
from sat_biblio_server import sat_biblio, json_result, EnregistrementDB, PACKDIR


@sat_biblio.route("/export/csv/", methods=["GET"])
def export_catalogue():
    """

    :return:
    """

    records_db = EnregistrementDB.query.all()

    path = os.path.join(PACKDIR, "static")
    filename_without_extension = f"catalogue-{datetime.datetime.now().isoformat().replace(':', '_')}"

    filename = ExportCatalogueManager.export_catalogue_csv(path, filename_without_extension, records_db)

    # return send_file(os.path.join("static", filename))  # json_result(True, records=records)

    return json_result(True, filename=os.path.basename(filename))


@sat_biblio.route("/export/xlsx/", methods=["GET"])
def export_catalogue_xlsx():
    """

    :return:
    """

    logging.error("records beginning")
    records_db = EnregistrementDB.query.all()

    path = os.path.join(PACKDIR, "static")
    filename_without_extension = f"catalogue-{datetime.datetime.now().isoformat().replace(':', '_')}"

    filename = ExportCatalogueManager.export_catalogue_xlsx(path, filename_without_extension, records_db)
    logging.error(filename)

    # return send_file(os.path.join("static", filename))  # json_result(True, records=records)
    return json_result(True, filename=os.path.basename(filename))  # json_result(True, records=records)
