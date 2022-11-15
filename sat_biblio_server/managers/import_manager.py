
import openpyxl

from sat_biblio_server.managers.catalogue_manager import CatalogueSchweitz, CatalogueHamelain1, \
    CatalogueHamelain2, CatalogueHamelain3


class ImportManager:

    @staticmethod
    def read_csv(filename: str):
        pass

    @staticmethod
    def read_xslx(filename: str, ignore_n_first_lines=0):
        work_book = openpyxl.load_workbook(filename=filename)
        current_sheet = work_book.active
        rows = [row for i, row in enumerate(current_sheet.iter_rows(values_only=True)) if i > ignore_n_first_lines and row[0] is not None and row[1] is not None]
        return rows

    @classmethod
    def import_schweitz_format(_cls, filename: str, ignore_n_first_lines=0):
        rows = _cls.read_xslx(filename)
        catalogue = CatalogueSchweitz()
        catalogue.parse_rows(rows)
        return catalogue

    @classmethod
    def import_hamelain_1(_cls, filename: str, ignore_n_first_lines=0):
        rows = _cls.read_xslx(filename)
        catalogue = CatalogueHamelain1()
        catalogue.parse_rows(rows, ignore_n_first_lines)
        return catalogue

        # excel_catalogue = openpyxl.load_workbook(filename)

    @classmethod
    def import_hamelain_2(_cls, filename: str, ignore_n_first_lines=0):
        # excel_catalogue = openpyxl.load_workbook(filename)
        rows = _cls.read_xslx(filename)
        catalogue = CatalogueHamelain2()
        catalogue.parse_rows(rows, ignore_n_first_lines)
        return catalogue

    @classmethod
    def import_hamelain_3(_cls, filename: str, ignore_n_first_lines=0):
        rows = _cls.read_xslx(filename)
        catalogue = CatalogueHamelain3()
        catalogue.parse_rows(rows, ignore_n_first_lines)
        return catalogue



