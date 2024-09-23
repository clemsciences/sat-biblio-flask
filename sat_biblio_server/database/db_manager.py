"""

"""

import datetime
import json
from flask_sqlalchemy import SQLAlchemy
from sat_biblio_server.utils import UserRight, DateHeureUtils

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


db = SQLAlchemy()


class JsonEncodedDict(db.TypeDecorator):
    @property
    def python_type(self):
        pass

    impl = db.String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


def row_to_dict(row):
    result = {}
    for c in row.__table__.columns:
        value = getattr(row, c.name)
        if c.name != "mdp_hash":
            if type(value) == UserRight:
                result[c.name] = value.name
            elif isinstance(value, datetime.datetime):
                dt = DateHeureUtils()
                dt.from_datetime(value)
                result[c.name] = dt.to_json()
            else:
                result[c.name] = value
    return result


def to_date(jour, mois, annee):
    jour_mois_annee = datetime.date(annee, mois, jour)
    return jour_mois_annee
