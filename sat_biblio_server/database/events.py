"""

"""

from sat_biblio_server.database.db_manager import db
from sat_biblio_server.utils import EventEnum


__author__ = ["Clément Besnier <clem@clementbesnier.fr"]


class LogEventDB(db.Model):
    __tablename__ = "LogEvent"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_type = db.Column(db.Enum(EventEnum))
    object_id = db.Column(db.Integer)
    event_datetime = db.Column(db.DateTime)
    event_owner_id = db.Column(db.Integer)
    table_name = db.Column(db.String(50))
    values = db.Column(db.String(500), nullable=True)

    # def __str__(self):
    #     return f"{self.event_type.name} {self.}"
    def __repr__(self):
        return f"{self.event_type}, {self.table_name}({self.object_id}), {self.event_type.isoformat()}"
