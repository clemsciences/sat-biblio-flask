"""

"""

import datetime

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from sat_biblio_server.database.db_manager import db

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

from sat_biblio_server.utils import UserRight


class UserDB(db.Model):
    """
    Un utilisateur est quelqu'un qui peut se connecter à l'interface web.

    Un gestionnaire est un resp

    Un bibliothécaire est une personne auqui est responsable des collections

    Un éditeur est une personne qui peut exporter les données dans un format utilisable.
    """
    __tablename__ = "User"
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = db.Column(db.String(50))
    family_name = db.Column(db.String(50))
    right = db.Column(db.Enum(UserRight))

    date_inscription = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(120), unique=True)
    # mdp = db.Column(db.String(80), unique=False, nullable=False)
    mdp_hash = db.Column(db.String(128), unique=False)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True, default=None)
    is_admin = db.Column(db.Boolean, nullable=True, default=False)
    link_to_validate = db.Column(db.String(64), nullable=True, default="")

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.mdp_hash = generate_password_hash(password)

    def set_confirmed(self, confirmed):
        self.confirmed = confirmed

    def set_confirmed_on(self, confirmed_on):
        self.confirmed_on = confirmed_on

    def verify_password(self, password):
        return check_password_hash(self.mdp_hash, password)

    @staticmethod
    def register(email, password):
        user = UserDB(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def __repr__(self):
        return '<User {0}>'.format(self.email)

    def generate_confirmation_token(self, expiration=3600):
        s = TimedJSONWebSignatureSerializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id}).decode("utf-8")

    def confirm(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.confirmed_on = datetime.datetime.utcnow()
        db.session.add(self)
        return True
