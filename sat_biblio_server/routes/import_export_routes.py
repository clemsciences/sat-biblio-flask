"""
This module does not affect the database
"""


import os

from flask import request, url_for, send_from_directory
from werkzeug.utils import secure_filename

from sat_biblio_server.managers.catalogue_manager import CatalogueConverter
from sat_biblio_server import sat_biblio, json_result
from sat_biblio_server.config.production import Config
from sat_biblio_server.managers.import_manager import ImportManager
from sat_biblio_server.managers.export_manager import ExportCatalogueManager


@sat_biblio.route("/import-export/process", methods=["POST"])
def process_import_export():
    if request.method == "POST":
        if "file" not in request.files:
            return json_result(False, message="Aucun fichier reçu")
        file = request.files["file"]

        if file:
            filename = secure_filename(file.filename)
            if not os.path.exists(Config.UPLOAD_FOLDER):
                os.makedirs(Config.UPLOAD_FOLDER)
            if os.path.exists(Config.UPLOAD_FOLDER):
                path_to_file = os.path.join(Config.UPLOAD_FOLDER, filename)
                file.save(path_to_file)

                # region
                data = request.form
                chosen_method = data.get("method", "0")
                path_to_new_catalogue = ""
                if chosen_method == "1":
                    imported_model = ImportManager.import_schweitz_format(path_to_file)
                    exported_model = CatalogueConverter.from_schweitz_to_hamelain_1(imported_model)
                    path_to_new_catalogue = ExportCatalogueManager.export_hamelain_1(Config.UPLOAD_FOLDER, exported_model)
                # elif chosen_method == "2":
                #     imported_model_1 = ImportManager.import_hamelain_1()
                #     imported_model_2 = ImportManager.import_hamelain_2()
                # endregion
                elif chosen_method == "2":
                    imported_model = ImportManager.import_schweitz_format(path_to_file)
                    pass
                elif chosen_method == "3":
                    imported_model = ImportManager.import_hamelain_3(path_to_file)
                    exported_model = CatalogueConverter.from_schweitz_to_hamelain_1(imported_model)
                    path_to_new_catalogue = ExportCatalogueManager.export_hamelain_1(Config.UPLOAD_FOLDER,
                                                                                     exported_model)
                    pass

                return json_result(True, filename=path_to_new_catalogue)
            else:
                return json_result(False, filename="No upload directory")

    return json_result(False), 200


@sat_biblio.route("/import-export/download/<string:filename>")
def serve_file(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)
