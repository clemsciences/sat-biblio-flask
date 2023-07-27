
import datetime

from sat_biblio_server.database.db_manager import db
from sat_biblio_server.database.users import UserDB


__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class ImportDB(db.Model):
    __tablename__ = "Import"
    __table_args__ = {'sqlite_autoincrement': True}
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(50), default="", nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_date = db.Column(db.DateTime)


    id_user = db.Column(db.Integer, db.ForeignKey("User.id"))
    user = db.relationship(UserDB, primaryjoin=id_user == UserDB.id)  # , on_delete=models.CASCADE)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default="", nullable=False)
    selected_method = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"{self.filename}-{self.start_date.isoformat()}-{self.end_date.isoformat()}"


class ImportedItemsDB(db.Model):
    __tablename__ = "ImportedItems"
    __table_args__ = {'sqlite_autoincrement': True}
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, nullable=False)
    table_name = db.Column(db.String(50), nullable=False)
    import_id = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f"{self.id_}-item:{self.item_id}-import:{self.import_id}"
