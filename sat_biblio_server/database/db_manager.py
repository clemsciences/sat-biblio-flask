"""

"""

import datetime
import json
import re
import unicodedata
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sat_biblio_server.utils import UserRight, DateHeureUtils

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


db = SQLAlchemy()


def update_date_derniere_modification(mapper, connection, target):
    if hasattr(target, 'date_derniere_modification'):
        target.date_derniere_modification = datetime.datetime.now()


def extract_year_from_text(value):
    """Renvoie la première année (18xx/19xx/20xx) trouvée dans une chaîne, sinon None.

    Le champ `annee_obtention` est un texte libre (ex. "achat 12.06.2012",
    "don Schweitz") : on en extrait une année pour permettre le filtrage.
    """
    if value is None:
        return None
    m = re.search(r"(?:18|19|20)\d{2}", str(value))
    return int(m.group(0)) if m else None


def text_sort_key(value):
    """Forme d'un texte pour le tri et la recherche : sans accents ni casse.

    SQLite compare les chaînes octet par octet : sans cela « éditions Perrin »
    ou « Œuvre des martyrs » seraient rangés après « Z ». On retire aussi la
    ponctuation de tête (« (Tours) », « . Recueil… »). Les chaînes vides et
    NULL donnent "".
    """
    if value is None:
        return ""
    s = str(value).casefold().replace("œ", "oe").replace("æ", "ae")
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    s = re.sub(r"\s+", " ", s)
    return re.sub(r"^[^\w]+", "", s).strip()


@event.listens_for(Engine, "connect")
def register_sqlite_functions(dbapi_connection, connection_record):
    """Enregistre les fonctions SQL personnalisées (disponibles pour SQLite)."""
    if hasattr(dbapi_connection, "create_function"):
        # Import paresseux : évite tout cycle d'import à l'initialisation du paquet.
        from sat_biblio_server.data.gazetteer import normalize_place
        dbapi_connection.create_function("extract_year", 1, extract_year_from_text)
        dbapi_connection.create_function("normalize_place", 1, normalize_place)
        dbapi_connection.create_function("sort_key", 1, text_sort_key, deterministic=True)


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
