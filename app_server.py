
import os
from sat_biblio_server.database import db
from sat_biblio_server import create_app
from sat_biblio_server.config.production import Config

app = create_app(Config)


@app.route("/health")
def health():
    """Lightweight liveness endpoint used by the Docker HEALTHCHECK."""
    return {"status": "ok"}, 200


with app.app_context():
    if not os.path.exists("/var/www/satbiblio.clementbesnier.eu/server/data-prod.sqlite3"):
        db.create_all()
