
import os
from sat_biblio_server.database import db
from sat_biblio_server import create_app

app = create_app()

with app.app_context():
    if not os.path.exists(os.path.join(os.path.join(os.path.dirname(__file__), "sat_biblio_server", "data-dev.sqlite3"))):
        db.create_all()
