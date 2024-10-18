import datetime
import os

from sat_biblio_server.data.models_2023 import Import, User2023
from sat_biblio_server.managers.import_manager import CatalogueFileManager, ImportManager2023
from sat_biblio_server import PACKDIR


from sat_biblio_server import create_app
from sat_biblio_server.config.development import Config
from sat_biblio_server.database.db_manager import db
try:
    from sat_biblio_server.create_admin_user import create_admin_user
except ImportError:
    create_admin_user = None

EMAIL_ADDRESS = ""

if __name__ == "__main__":
    database_filename = "data-dev.sqlite3"
    if os.path.exists(os.path.join(PACKDIR, database_filename)):
        os.remove(os.path.join(PACKDIR, database_filename))
        print("deleted")
    else:
        print("does not exist")

    app = create_app(Config)

    with app.app_context() as c:
        db.create_all()
        if create_admin_user:
            create_admin_user(db)

        # path_to_catalogues = os.path.join(PACKDIR, "..", CatalogueFileManager.UPLOAD_FOLDER)
        path_to_catalogues = os.path.join(CatalogueFileManager.UPLOAD_FOLDER)
        for filename in os.listdir(path_to_catalogues):
            print(f"filename: {filename}")
            description = ""
            catalogue_file = CatalogueFileManager.extract_from_filename(filename)
            # full_path =
            # rows_to_preview_number = data.get("rowsToPreviewNumber", 0)
            first_rows_to_ignore_number = 0
            start_date = datetime.datetime.utcnow()
            id_user = User2023.from_email_address_to_user(EMAIL_ADDRESS).get("id", "")

            # selected_method = data.get("selected_method", "0")
            ignore_n_first_lines = 0
            # status = "to-do"
            key = catalogue_file.key
            path_to_file = CatalogueFileManager.get_catalogue_path(key)
            # file_check = ImportManager2023.check_2023_column_names(path_to_file)
            # print(f"path_to_file {path_to_file} {key}")
            catalogue = ImportManager2023.parse_file_to_catalogue_2023(path_to_file, ignore_n_first_lines)

            # if file_check is None:
            #     return json_result(False, message="")
            # if len(file_check) != len(catalogue.column_names):
            #     return json_result(False, message=f"Erreur dans l'ordre des colonnes : {file_check}")
            ImportManager2023.import_catalogue_to_db(catalogue)

            import_db = Import.from_data_to_db(dict(filename=filename,
                                                    selected_method="script",
                                                    start_date=start_date,
                                                    end_date=datetime.datetime.utcnow(),
                                                    description=description,
                                                    status="",
                                                    id_user=id_user,
                                                    ))
            Import.save_import(import_db)
