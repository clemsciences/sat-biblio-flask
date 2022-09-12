"""

"""
import datetime
import dbm

from flask import jsonify
import os

from sat_biblio_server.data.models import ReferenceBibliographiqueLivre
from sat_biblio_server.database.db_manager import db
from sat_biblio_server import create_app, sat_biblio, UserDB
from sat_biblio_server.config.development import Config
try:
    from sat_biblio_server.create_admin_user import create_admin_user
except ImportError:
    create_admin_user = None

# @sat_biblio.route("/test")
# def api_test():
#     return jsonify({"success": True, "message": "Test succeeded"})


# @sat_biblio.route("/")
# def api_redirect():
#     return jsonify({"success": False, "message": "Vous n'êtes pas connecté. Veuillez vous connecter pour continuer."})
from sat_biblio_server.utils import UserRight

app = create_app(Config)

with app.app_context():
    # print(os.path.join(os.path.join(os.path.dirname(__file__), "sat_biblio_server", "data-dev.sqlite3")))
    print(os.path.join(os.path.join(os.path.dirname(__file__))))
    if not os.path.exists(
            os.path.join(os.path.join(os.path.dirname(__file__), "data-dev.sqlite3"))):
        db.create_all()
        if create_admin_user:
            create_admin_user(db)
        # define_admin(db)
        # print("ok")

if __name__ == '__main__':
    # app.register_blueprint(sat_biblio, url_prefix="/api")
    app.run(debug=True, port=5000)
