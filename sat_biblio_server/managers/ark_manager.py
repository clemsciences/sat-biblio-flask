
import arkpy
from sat_biblio_server.database.books_2023 import (
    Author2023DB,
    ReferenceBibliographiqueLivre2023DB,
    Enregistrement2023DB)
from sat_biblio_server.database import db


class ArkManager:

    AUTHORITY = "satbiblio"
    # TEMPLATE = "eeeeeeeek"
    TEMPLATE = "eeeeeeee"
    PREFIX = "bb0"

    RESOURCES_TABLES = [Author2023DB, ReferenceBibliographiqueLivre2023DB, Enregistrement2023DB]

    @classmethod
    def is_ark_unique(cls, ark_name: str):
        for table in cls.RESOURCES_TABLES:
            if table.query.filter_by(ark_name=ark_name).exists():
                return False
        return True

    @classmethod
    def load_all_ark_names(cls):
        """
        >>> from sat_biblio_server import create_app
        >>> from sat_biblio_server.config.development import Config
        >>> app = create_app(Config)
        >>> with app.app_context():
        ...     ArkManager.load_all_ark_names()

        :return:
        """
        ark_names = []
        for resource in cls.RESOURCES_TABLES:
            ark_names.extend([i[0] for i in db.session.query(resource.ark_name).all() if i[0]])
        return ark_names

    @classmethod
    def is_ark_valid(cls, ark: str):
        return arkpy.validate(ark)

    @classmethod
    def generate_ark(cls):
        return arkpy.mint(cls.AUTHORITY, cls.TEMPLATE, cls.PREFIX)

    @classmethod
    def ark_name_generator(cls):
        ark_names = cls.load_all_ark_names()
        while True:
            generated_ark_name = cls.generate_ark()
            if generated_ark_name not in ark_names:
                yield generated_ark_name
                ark_names.append(generated_ark_name)

    @classmethod
    def __reset_ark_names(cls):
        for table in cls.RESOURCES_TABLES:
            for resource in db.session.query(table).all():
                new_ark_name = None
                resource.ark_name = new_ark_name
                db.session.commit()

    @classmethod
    def give_ark_names(cls):
        """
        >>> from sat_biblio_server import create_app
        >>> from sat_biblio_server.config.development import Config
        >>> app = create_app(Config)
        >>> with app.app_context():
        ...     ArkManager.give_ark_names()
        ...     ArkManager.load_all_ark_names()

        :return:
        """
        generator = cls.ark_name_generator()
        for table in cls.RESOURCES_TABLES:
            for resource in db.session.query(table).filter_by(ark_name=""):
                new_ark_name = next(generator)
                resource.ark_name = new_ark_name
                db.session.commit()

    @classmethod
    def get_resource(cls, ark_name):
        for table in cls.RESOURCES_TABLES:
            resource_db = db.session.query(table).filter_by(ark_name=ark_name).first()
            if resource_db:
                return dict(id=resource_db.id, table_name=table.__tablename__)
        return None
