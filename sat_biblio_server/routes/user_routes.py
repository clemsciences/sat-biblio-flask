"""

"""

from datetime import timedelta
import json
import random

from flask import session, request
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token, decode_token
from sqlalchemy import or_
from werkzeug.security import generate_password_hash

from routes import validation_connexion_et_retour_defaut
from sat_biblio_server import sat_biblio, UserDB, db
import sat_biblio_server.data.validation as dv
import sat_biblio_server.database as dbm
from sat_biblio_server.managers import mail_manager
import sat_biblio_server.sessions.session_manager as sm
from sat_biblio_server.utils import json_result


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region connexion
def connect_user_login(user: UserDB, token: str):
    if login_user(user):
        session["email"] = user.email
        session["first_name"] = user.first_name
        session["family_name"] = user.family_name
        session["right"] = user.right.value
        session["token"] = token


@sat_biblio.route("/users/connect", methods=["POST"])
def login():
    data = request.get_json()
    return connect_user(data)


def connect_user(data):
    """

    :param data: request data
    :return:
    """
    if dv.check_user_connection(data):
        user, message = UserDB.authenticate(**data)
        if not user:
            return json_result(False,
                               message=message,
                               connected=False), 401

        expires_duration = timedelta(hours=4)
        token = create_access_token(identity=user.email,
                                    fresh=True,
                                    expires_delta=expires_duration)
        print("created_token", token)
        connect_user_login(user, token)

        print("bien connecté")
        return json_result(True,
                           message="Vous êtes bien connecté.",
                           connected=True,
                           connectionInfo={
                               "token": session["token"],
                               "email": session["email"],
                               "first_name": session["first_name"],
                               "family_name": session["family_name"],
                               "right": session["right"]
                           }), 200


def disconnect_user():
    if logout_user():
        if "email" in session:
            del session["email"]
        if "first_name" in session:
            del session["first_name"]
        if "family_name" in session:
            del session["family_name"]
        if "right" in session:
            del session["right"]
        if "token" in session:
            del session["token"]
    else:
        print("strange")


@sat_biblio.route("/users/confirm/<inscription_token>", methods=["GET"])
def confirmer_inscription_utilisateur(inscription_token):
    email = request.args.get("email")
    user_sess = sm.UserSess(email)
    if user_sess and user_sess.confirmer_token(inscription_token):
        token = create_access_token(identity=user_sess.user_db.email)
        connect_user_login(user_sess.user_db, token)
        return json_result(True,
                           message="Votre compte est validé.",
                           connected=True,
                           connectionInfo={
                               "token": session["token"],
                               "email": session["email"],
                               "first_name": session["first_name"],
                               "family_name": session["family_name"],
                               "right": session["right"]
                           }), 200
    else:
        return json_result(False, message="Le lien donné est invalide. "
                                          "Veuillez contacter l'administrateur si vous pensez qu'il y a un problème.")


# @sat_biblio.route("/user/confirmed", methods=["GET"])
# def est_utilisateur_confirme():
#     email = request.args.get("email")
#     return jsonify({"success": True})
#     return render_template("patient/connexion/pas_confirme_patient.html", link=email)
#
#
# @sat_biblio.route("/pas_connecte_patient")
# def pas_connecte_patient():
#     return render_template("patient/connexion/pas_connecte_patient.html")


# @login_required
@sat_biblio.route("/users/disconnect", methods=["GET"])
# @jwt_required
def logout():
    if "email" in session:
        disconnect_user()
    return json_result(True, message="Vous êtes correctement déconnecté.")


@sat_biblio.route("/users/create", methods=["POST"])
def create_new_user():
    if request.method == "POST":
        user_form = request.get_json()
        if dv.check_user(user_form):
            already_exists = sm.Users.check_if_user_exist(user_form["email"]) is not None
            if already_exists:
                return json_result(False,
                                   message="Il existe déjà un compte avec cet adresse email.")
            else:
                user = sm.UserSess.create_new(user_form, generate_password_hash(user_form["password"]))
                # print("Créer nouvel utilisateur")
                if user:
                    token = user.generate_confirmation_token()
                    # satbibilio.clementbesnier.eu/utilisateur/enregistre
                    link = f"https://satbibilio.clementbesnier.eu/utilisateur/verification-enregistrement?" \
                           f"inscription_token={token}&email={user.email}"
                    # link = url_for("sat_biblio.confirmer_inscription_utilisateur",
                    #                inscription_token=token,
                    #                email=user.email,
                    #                _external=True)
                    link_to_resend = ""
                    mail_manager.envoyer_mail_demande_inscription_utilisateur(user, link)
                    return json_result(True,
                                       message="Le compte a correctement été créé.",
                                       link_to_resend=link_to_resend)
                else:
                    return json_result(False, message="Les données reçues sont invalides")
    return json_result(False)


@sat_biblio.route("/users/validation_inscription_patient/<string:link>", methods=["GET"])
def valider_inscription(link):
    user = sm.Users.load_user_by_validation_link(link)
    if user is None:
        return json_result(False)
    else:
        sm.Users.validate_user(user)
        return json_result(True)


@sat_biblio.route("/users/check_login", methods=["POST"])
def check_login():
    if "email" in session:
        return json_result(True,
                           connected=True,
                           message="Vous êtes connecté",
                           connectionInfo=dict(
                               token=session["token"],
                               email=session["email"],
                               first_name=session["first_name"],
                               family_name=session["family_name"],
                               right=session["right"]),
                           )
    else:
        return json_result(False,
                           connected=False,
                           message="Vous êtes déconnecté")


@sat_biblio.after_request
def add_connection_hints(response):
    print(response.get_json())
    if response.get_json():
        d = response.get_json()
        d["connected"] = "email" in session
        response.set_data(json.dumps(d))
    return response


@sat_biblio.route("/users/search-near")
def search_near_users():
    query_result = request.args.get("user")
    res = []
    users_db = dbm.UserDB.query.filter(
        or_(dbm.UserDB.first_name.like(f"%{query_result}%"),
            dbm.UserDB.family_name.like(f"%{query_result}%"))).all()
    for user_db in users_db:
        res.append(dict(text=f"{user_db.first_name} {user_db.family_name}",
                        value=user_db.id))
    return json_result(True, suggestedUsers=res), 200


def generate_new_password(password_length=10):
    """
    Generate a new password.
    :return: new password
    """
    password = []
    for i in range(password_length):
        password.append(random.choice(["azertyuiopqsdfghjklmwxcvbn1234567890"]))
    return "".join(password)


@sat_biblio.route("/users/forgotten-password")
@validation_connexion_et_retour_defaut("email", ["GET"])
def send_forgotten_password_email():
    """
    Send an email to a user with a new password.
    :return:
    """
    data = request.get_json()
    if "email_address" in data:
        user_db = UserDB.query.filter_by(email=session["email"]).first()
        if not user_db:
            return json_result(False, "L'adresse email donné est inconnu"), 200
        new_password = generate_new_password()
        new_password_hash = generate_password_hash(new_password)
        user_db.mdp_hash = new_password_hash
        db.session.commit()
        mail_manager.send_email_new_password(session["email"], new_password)
        return json_result(True, "Un courriel vous a été envoyé"), 200
    return json_result(False, "Il manque l'adresse email dans la requête"), 401


@sat_biblio.route("/users/new-password", methods=["POST"])
def set_new_password():
    """
    Change password for a user.
    :return:
    """
    data = request.get_json()
    if "currentPassword" in data and "newPassword" in data:
        current_password = data["currentPassword"]
        new_password = data["newPassword"]
        user_db = UserDB.query.filter_by(email=session["email"]).first()
        if not user_db:
            return json_result(False, message="L'utilisateur n'a pas été trouvé."), 200
        if not user_db.verify_password(current_password):
            return json_result(False, message="Le mot de passe actuel est incorrect."), 200
        if len(new_password) < 6:
            return json_result(False, message="Le nouveau mot de passe proposé est trop court. "
                                              "Il doit avoir une taille de 6 caractères au minimum."), 200
        new_password_hash = generate_password_hash(new_password)
        user_db.mdp_hash = new_password_hash
        db.session.commit()
        return json_result(True, message="Le nouveau mot de passe a été accepté."), 200
    return json_result(False, "La requête est incorrect"), 400
# endregion
