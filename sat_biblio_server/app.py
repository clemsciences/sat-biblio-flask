"""

"""

from flask import jsonify
import os

from sat_biblio_server.database.db_manager import db
from sat_biblio_server import create_app, sat_biblio
from sat_biblio_server.config.development import Config


@sat_biblio.route("/test")
def test():
    return jsonify({"success": True, "message": "Test succeeded"})


@sat_biblio.route("/")
def api_redirect():
    return jsonify({"success": False, "message": "Vous n'êtes pas connecté. Veuillez vous connecter pour continuer."})


app = create_app(Config)


with app.app_context():
    # print(os.path.join(os.path.join(os.path.dirname(__file__), "sat_biblio_server", "data-dev.sqlite3")))
    if not os.path.exists(os.path.join(os.path.join(os.path.dirname(__file__), "sat_biblio_server", "data-dev.sqlite3"))):
        db.create_all()
        # define_admin(db)
        # print("ok")

if __name__ == '__main__':

    # app.register_blueprint(sat_biblio, url_prefix="/api")
    app.run(debug=True, host="0.0.0.0", port=5000)
