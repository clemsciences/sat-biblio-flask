import datetime

import sat_biblio_server.database as dbm

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

from sat_biblio_server.utils import UserRight

engine = dbm.db.create_engine('sqlite:///sqlalchemy_example.db', echo=True)
DBSession = dbm.db.sessionmaker(bind=engine)
db_session = DBSession()


class UserConnection:
    pass


class Users:

    def __init__(self):
        self.identifiants = []

    @staticmethod
    def load_user_by_validation_link(link):
        return dbm.UserDB.query.filter_by(link_to_validate=link).first()

    @staticmethod
    def validate_user(user: dbm.UserDB):
        user.link_to_validate = ""
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        dbm.db.session.commit()

    @staticmethod
    def check_if_user_exist(email_address: str):
        return dbm.UserDB.query.filter_by(email=email_address).first()


class UserSess:

    def __init__(self, email):
        self.username = email
        self.user_db = dbm.UserDB.query.filter_by(email=email).first()

    @staticmethod
    def create_new(form, mdp_hash):
        new_user = dbm.UserDB(first_name=form["first_name"],
                              family_name=form["family_name"],
                              right=UserRight.lecteur,
                              email=form["email"],
                              mdp_hash=mdp_hash,
                              date_inscription=datetime.datetime.now())
        dbm.db.session.add(new_user)
        dbm.db.session.commit()
        return new_user

    def update_profile(self):
        # TODO
        pass

    def update_user_password(self, mdp_hash):
        self.user_db.mdp_hash = mdp_hash
        dbm.db.session.commit()

    def delete_user(self):
        dbm.UserDB.query.filter_by(id=self.user_db.get_id()).delete()
        dbm.db.session.commit()

    def confirmer_token(self, token):
        if self.user_db.confirm(token):
            self.user_db.confirmed = True
            self.user_db.confirmed_on = datetime.datetime.utcnow()
            dbm.db.session.commit()
            return True
        else:
            return False

    def regenerate_token(self, expiration):
        return self.user_db.generate_confirmation_token(expiration)

