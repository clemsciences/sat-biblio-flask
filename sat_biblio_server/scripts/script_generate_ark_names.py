"""Give an ARK name to every resource that needs one."""

from managers.ark_manager import ArkManager
from sat_biblio_server import create_app
from sat_biblio_server.config.production import Config
# from sat_biblio_server.config.development import Config


app = create_app(Config)

with app.app_context() as c:
    ArkManager.give_ark_names()
