
import openpyxl

from managers.catalogue_manager import CatalogueSchweitz


class ImportManager:

    @staticmethod
    def read_csv(filename: str):
        pass

    @staticmethod
    def read_xslx(filename: str):
        work_book = openpyxl.load_workbook(filename=filename)
        current_sheet = work_book.active
        rows = [row for row in current_sheet.iter_rows(values_only=True) if row[0] is not None and row[1] is not None]
        return rows

    @classmethod
    def import_schweitz_format(_cls, filename: str, ):
        rows = _cls.read_xslx(filename)
        catalogue = CatalogueSchweitz()
        catalogue.parse_rows(rows)
        return catalogue

    @staticmethod
    def import_hamelain_format():
        pass

