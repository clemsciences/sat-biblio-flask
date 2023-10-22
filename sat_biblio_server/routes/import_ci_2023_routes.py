"""
import_ci_2023_routes.py ->
ci -> catalogue-inventaire

Voir

"""


import datetime
import os

from flask import request, session

from sat_biblio_server.config.production import Config
from sat_biblio_server.managers.export_manager import ExportCatalogueManager
from sat_biblio_server.routes import validation_connexion_et_retour_defaut
from sat_biblio_server.managers.catalogue_manager import Catalogue2023, Catalogue2023Row
from sat_biblio_server.database import db, ImportDB
from sat_biblio_server.managers.import_manager import ImportManager2023, CatalogueFileManager, CsvReader
# from sat_biblio_server.data.models import Author, ReferenceBibliographiqueLivre, Enregistrement, Import
from sat_biblio_server import sat_biblio, json_result
from sat_biblio_server.data.models_2023 import Import, User2023


# region catalogue
class CatalogueAction:
    check = "check"
    import_catalogue = "import_catalogue"
    preview = "preview"
    download = "download"
    info = "info"
    to_fix = "to-fix"


@sat_biblio.route("/import-ci-2023/catalogues/<string:key>/", methods=["GET", "DELETE"])
@validation_connexion_et_retour_defaut("email", ["DELETE"])
def manage_ci_2023_catalogue(key):
    """
    GET:
     - check:
     - preview:
     - info:
    DELETE: delete catalogue

    :param key: key of the catalogue
    :return: response
    """
    if request.method == "GET":
        action = request.args.get("action", "")
        if action == CatalogueAction.check:
            ignore_n_first_rows = int(request.args.get("ignore_n_first_rows", 1))
            path_to_file = CatalogueFileManager.get_catalogue_path(key)
            try:
                file_check = ImportManager2023.check_2023_column_names(path_to_file, ignore_n_first_rows)
            except ValueError:
                return json_result(True, file_check=False, message="")
            return json_result(True, file_check=file_check)
            pass
        elif action == CatalogueAction.preview:
            ignore_n_first_rows = int(request.args.get("ignore_n_first_rows", 1))
            n_first_rows = int(request.args.get("n_first_rows", 1))
            filter_by_verified_entry = int(request.args.get("filter_by_verified_entry", 0))
            # print(f"filter_by_verified_entry={filter_by_verified_entry}")
            first_rows = CatalogueFileManager.get_first_row(key, ignore_n_first_rows, n_first_rows)
            path_to_file = CatalogueFileManager.get_catalogue_path(key)
            try:
                file_check = ImportManager2023.check_2023_column_names(path_to_file)
                catalogue = ImportManager2023.parse_file_to_catalogue_2023(path_to_file, ignore_n_first_rows)
                if filter_by_verified_entry == 1:
                    number_of_rows = len(catalogue.rows_filtered_by_verified_entry)
                else:
                    number_of_rows = len(catalogue.rows)
                column_reference = Catalogue2023.COLUMNS
                actual_columns = CsvReader.get_row(path_to_file, ignore_n_first_rows)
                return json_result(True, first_rows=first_rows,
                                   check=file_check,
                                   column_reference=column_reference,
                                   actual_columns=actual_columns,
                                   number_of_rows=number_of_rows)
            except ValueError:
                return json_result(False, check=False)
        elif action == CatalogueAction.info:
            path_to_file = CatalogueFileManager.get_catalogue_filename(key)
            info = CatalogueFileManager.extract_from_filename(path_to_file)
            return json_result(True, info=info, path=path_to_file)
        elif action == CatalogueAction.to_fix:
            # path_to_file = CatalogueFileManager.get_catalogue_filename(key)
            path_to_file = CatalogueFileManager.get_catalogue_path(key)
            print(path_to_file)
            catalogue = ImportManager2023.parse_file_to_catalogue_2023(path_to_file)
            # new_path_to_file = os.path.join(os.path.dirname(path_to_file), "to-fix.xslx")
            filename_without_extension = os.path.basename(path_to_file)[:-5]
            new_path_to_file = ExportCatalogueManager.export_2023(os.path.dirname(path_to_file),
                                                                  catalogue, title="To fix",
                                                                  filename_prefix=f"{filename_without_extension}-",
                                                                  protected=False)

            # xlsx_file_content = CsvReader.get_current_sheet(path_to_file)
            # # checks = []
            # for row in xlsx_file_content.iter_rows():
            #     # print(dir(row))
            #     # print(row)
            #     row_2023 = Catalogue2023Row()
            #     row_2023.parse_row([cell.value for cell in row])
            #     # check = row_2023.check_row()
            #     # checks.append(check)

            link_to_download = os.path.join(Config.UPLOAD_FOLDER, new_path_to_file)
            return json_result(True, linkToDownload=link_to_download)

    elif request.method == "DELETE":
        existed = CatalogueFileManager.delete_catalogue(key)
        return json_result(existed, message="Catalogue deleted")
    return json_result(False)


@sat_biblio.route("/import-ci-2023/catalogues/", methods=["POST", "GET"])
@validation_connexion_et_retour_defaut("email", ["POST"])
def manage_ci_2023_catalogues():
    """
    POST: upload a new catalogue.
    GET: load the list of catalogues with pagination

    :return: response
    """
    if request.method == "POST":
        if "file" not in request.files:
            return json_result(False, message="Aucun fichier reçu")
        file = request.files["file"]
        if file:
            key = CatalogueFileManager.save_downloaded_file(file)
            return json_result(True, key=key)
        return json_result(False, message="No file")
    elif request.method == "GET":
        n_page = int(request.args.get("page", 0))
        size = int(request.args.get("size", 10))
        catalogues = CatalogueFileManager.get_catalogue_list(n_page, size)
        return json_result(True, catalogues=catalogues)
    return json_result(False, "Wrong request")


@sat_biblio.route("/import-ci-2023/catalogues/count/", methods=["GET"])
def get_ci_2023_catalogues_count():
    """
    GET: the total number of catalogues

    :return: response
    """
    total_count = CatalogueFileManager.get_catalogue_count()

    return json_result(True, total_count=total_count)

# endregion


# region imports
@sat_biblio.route("/import-ci-2023/", methods=["GET", "POST"])
@validation_connexion_et_retour_defaut("email", ["POST"])
def imports_ci_2023():
    """
    GET: get the list of imports with pagination and 'description' filtering
    POST: add a new import
    :return: response
    """
    if request.method == "GET":
        # Get all imports
        description = request.args.get("description", "")
        n_page = request.args.get("n_page", 0)
        size = request.args.get("size", 10)
        imports_list = Import.get_all_imports(description, n_page, size)
        return json_result(True, importList=imports_list)

    elif request.method == "POST":
        # data = request.form
        # key = data.get("key", "")

        # filename = CatalogueFileManager.get_catalogue_filename(key)
        print(request.get_json())
        data = request.get_json()

        # region
        description = data.get("description", "")
        filename = data.get("filename", "")
        path_to_new_catalogue = data.get("fullpath", "")
        # full_path =
        # rows_to_preview_number = data.get("rowsToPreviewNumber", 0)
        first_rows_to_ignore_number = data.get("firstRowsToIgnoreNumber", 0)
        start_date = datetime.datetime.utcnow()
        id_user = session.get("id", -1)

        # selected_method = data.get("selected_method", "0")
        ignore_n_first_lines = data.get("ignore_n_first_lines", 1)
        # status = "to-do"
        key = data.get("key", "")
        path_to_file = CatalogueFileManager.get_catalogue_path(key)
        # file_check = ImportManager2023.check_2023_column_names(path_to_file)
        print(f"path_to_file {path_to_file}")
        catalogue = ImportManager2023.parse_file_to_catalogue_2023(path_to_file, ignore_n_first_lines)

        # if file_check is None:
        #     return json_result(False, message="")
        # if len(file_check) != len(catalogue.column_names):
        #     return json_result(False, message=f"Erreur dans l'ordre des colonnes : {file_check}")
        ImportManager2023.import_catalogue_to_db(catalogue)

        import_db = Import.from_data_to_db(dict(filename=filename,
                                    selected_method="",
                                    start_date=start_date,
                                    end_date=datetime.datetime.utcnow(),
                                    description=description,
                                    status="",
                                    id_user=id_user,
                                    ))
        Import.save_import(import_db)
        # endregion
        return json_result(True, filename=path_to_new_catalogue)


@sat_biblio.route("/import-ci-2023/keys/<string:key>/", methods=["GET"])
def get_import_data_by_catalogue_key_request(key):
    """
    GET: get import data by catalogue key

    :return: response
    """

    filename = CatalogueFileManager.get_catalogue_filename(key)
    long_filename = CatalogueFileManager.extract_from_filename(filename)
    if long_filename:
        import_data = Import.get_import_by_filename(long_filename["filename"])
        return json_result(True, import_data=import_data, filename=filename)
    return json_result(False)


@sat_biblio.route("/import-ci-2023/count/", methods=["GET"])
def imports_ci_2023_count():
    """
    GET: get the total number of imports and the filtered count

    :return: response
    """
    description = ""
    the_filtered_query = ImportDB.query
    the_total_query = ImportDB.query
    if description:
        the_filtered_query = the_filtered_query.filter(ImportDB.description.like(f"%{description}%"))

    filtered_count = the_filtered_query.count()
    total_count = the_total_query.count()

    return json_result(True, total_count=total_count, filtered_count=filtered_count)

@sat_biblio.route("/import-ci-2023/<int:import_id>/", methods=["GET", "PUT", "DELETE"])
def import_ci_2023(import_id):
    """
    GET: get the import by id
    PUT: update the import info by id
    DELETE: delete an import by id
    :param import_id:
    :return: response
    """
    if request.method == "GET":
        # Get details of a previous import
        import_db = Import.get_import_db_by_id(import_id)
        if import_db:
            import_data = Import.from_db_to_data(import_db)
            user_data = User2023.from_db_to_data(import_db.user)
            # import_data = Import.get_import_by_filename(import_id)
        else:
            import_data = None
            user_data = None
        if import_data:
            return json_result(True, import_data=import_data, user_data=user_data)
        return json_result(False)
    elif request.method == "PUT":
        db.session.commit()

        pass
    elif request.method == "DELETE":
        pass
    return json_result(True), 200


# @sat_biblio.route("/import-ci-2023/upload/", methods=["GET", "PUT", "DELETE"])
# def upload_ci_2023():
#     if request.method == "POST":
#         if "file" not in request.files:
#             return json_result(False, message="Aucun fichier reçu")
#         file = request.files["file"]
#
#         if file:
#             filename = secure_filename(file.filename)
#             if not os.path.exists(Config.UPLOAD_FOLDER):
#                 os.makedirs(Config.UPLOAD_FOLDER)
#             if os.path.exists(Config.UPLOAD_FOLDER):
#                 path_to_file = os.path.join(Config.UPLOAD_FOLDER, filename)
#                 file.save(path_to_file)
#
#                 # region
#                 data = request.form
#                 chosen_method = data.get("method", "0")
#                 path_to_new_catalogue = ""
#                 if chosen_method == "1":
#                     imported_model = ImportManager.import_schweitz_format(path_to_file)
#                     exported_model = CatalogueConverter.from_schweitz_to_hamelain_1(imported_model)
#                     path_to_new_catalogue = ExportCatalogueManager.export_hamelain_1(Config.UPLOAD_FOLDER,
#                                                                                      exported_model)
#                 # elif chosen_method == "2":
#                 #     imported_model_1 = ImportManager.import_hamelain_1()
#                 #     imported_model_2 = ImportManager.import_hamelain_2()
#                 # endregion
#                 elif chosen_method == "2":
#                     imported_model = ImportManager.import_schweitz_format(path_to_file)
#                     pass
#                 elif chosen_method == "3":
#                     imported_model = ImportManager.import_hamelain_3(path_to_file)
#                     exported_model = CatalogueConverter.from_schweitz_to_hamelain_1(imported_model)
#                     path_to_new_catalogue = ExportCatalogueManager.export_hamelain_1(Config.UPLOAD_FOLDER,
#                                                                                      exported_model)
#                     pass
#
#                 return json_result(True, filename=path_to_new_catalogue)
#             else:
#                 return json_result(False, filename="No upload directory")
#
#     return json_result(False), 200
# endregion