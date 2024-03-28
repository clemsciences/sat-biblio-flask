
import arkpy
from sat_biblio_server.database.books_2023 import (
    Author2023DB,
    ReferenceBibliographiqueLivre2023DB,
    Enregistrement2023DB)


class ArkManager:

    AUTHORITY = ""
    TEMPLATE = ""

    @classmethod
    def is_ark_unique(cls, ark: str):
        if Author2023DB.query.filter_by(ark=ark).exists():
            return False
        elif ReferenceBibliographiqueLivre2023DB.query.filter_by(ark=ark).exists():
            return False
        elif Enregistrement2023DB.query.filter_by(ark=ark).exists():
            return False

    @classmethod
    def is_ark_valid(cls, ark: str):
        return arkpy.validate(ark)

    @classmethod
    def generate_ark(cls):
        return arkpy.mint(cls.AUTHORITY, "")
