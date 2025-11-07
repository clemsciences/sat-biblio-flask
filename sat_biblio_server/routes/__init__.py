"""

"""

from flask import Blueprint
from json import JSONEncoder
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
from sat_biblio_server.routes.record_with_reference_routes import *
from sat_biblio_server.routes.admin_routes import *
from sat_biblio_server.routes.import_routes import *
from sat_biblio_server.routes.export_routes import *
from sat_biblio_server.routes.event_routes import *
from sat_biblio_server.routes.borrowing_routes import *
from sat_biblio_server.routes.bnf_routes import *
from sat_biblio_server.routes.import_export_routes import *
from sat_biblio_server.routes.search_routes import *
from sat_biblio_server.routes.work_routes import *
from sat_biblio_server.routes.import_ci_2023_routes import *
from sat_biblio_server.routes.ark_routes import *
from sat_biblio_server.routes.sat_subscription_routes import *
