"""

"""

import datetime

from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from sat_biblio_server.database.db_manager import db
from sat_biblio_server.utils import UserRight

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class UserDB(db.Model):
    """
    Un utilisateur est quelqu'un qui peut se connecter à l'interface web.

    Un gestionnaire est un resp

    Un bibliothécaire est une personne qui est responsable des collections

    Un éditeur est une personne qui peut exporter les données dans un format utilisable.
    """
    __tablename__ = "User"
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = db.Column(db.String(50))
    family_name = db.Column(db.String(50))
    right = db.Column(db.Enum(UserRight))

    date_inscription = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # mdp = db.Column(db.String(80), unique=False, nullable=False)
    mdp_hash = db.Column(db.String(4096), unique=False, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True, default=None)
    is_admin = db.Column(db.Boolean, nullable=True, default=False)
    link_to_validate = db.Column(db.String(512), nullable=True, default="")

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

    def get_right(self):
        return self.right

    @staticmethod
    def register(email, password):
        user = UserDB(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")
        if not email:
            print("identification a échoué")
            message = "L'adresse email ou le mot de passe est incorrect."
            return None, message
        user = cls.query.filter_by(email=email).first()

        if not password:
            message = "Aucun mot de passe."
            return None, message

        if not user:
            message = "L'adresse email est inconnue."
            return None, message

        if not user.verify_password(password):
            print("mauvais mot de passe")
            message = "L'adresse email ou le mot de passe est incorrect."
            return None, message

        if not user.confirmed:
            print("utilisateur non confirmé")
            message = "L'utilisateur n'est pas confirmé."
            return None, message

        return user, ""

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def __repr__(self):
        return f"<User {self.email}>"

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], str(expiration))
        return s.dumps({"confirm": self.id})

    def confirm(self, token, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], str(expiration))
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

    def pretty_string(self):
        return f"{self.first_name} {self.family_name} ({self.email})"
