"""

"""

from flask import Blueprint
from flask.json import JSONEncoder
# from app.database_manager import JsonEncodedDict


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        JSONEncoder.default(self, obj)


Blueprint.json_encoder = CustomJSONEncoder

from sat_biblio_server.routes.check_routes import *
from sat_biblio_server.routes.contact_routes import *
from sat_biblio_server.routes.user_routes import *
from sat_biblio_server.routes.book_routes import *
from sat_biblio_server.routes.author_routes import *
from sat_biblio_server.routes.reference_routes import *
from sat_biblio_server.routes.record_routes import *
from sat_biblio_server.routes.admin_routes import *
from sat_biblio_server.routes.import_routes import *
