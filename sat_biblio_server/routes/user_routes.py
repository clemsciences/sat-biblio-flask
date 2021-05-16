"""

"""

from datetime import datetime, timedelta
from functools import wraps
import json

from flask import url_for, session, request, jsonify
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
import jwt
from sqlalchemy import or_
from werkzeug.security import generate_password_hash

from sat_biblio_server import sat_biblio, UserDB, jwt, Config
from sat_biblio_server.data.models import User
from sat_biblio_server.managers import mail_manager
import sat_biblio_server.database as dbm
import sat_biblio_server.sessions.session_manager as sm
import sat_biblio_server.data.validation as dv
from sat_biblio_server.utils import json_result


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region connexion

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, Config.JWT_SECRET_KEY)
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


def connect_user_login(user: UserDB):
    if login_user(user):
        session["email"] = user.email
        session["first_name"] = user.first_name
        session["family_name"] = user.family_name
        session["right"] = user.right.value


@sat_biblio.route("/users/connect", methods=["POST"])
def connect_user():
    if "email" in session:
        return json_result(True, message="Connexion réussie", token="", connectionInfo={
            "email": session["email"],
            "first_name": session["first_name"],
            "family_name": session["family_name"],
            "right": session["right"]}, connected=True)
    else:
        data = request.get_json()
        if dv.check_user_connection(data):
            user, message = UserDB.authenticate(**data)
            if not user:
                return json_result(False, message=message), 401

            connect_user_login(user)

            token = create_access_token(identity=user.email)

            print("bien connecté")
            return json_result(True, message="Vous êtes bien connecté.",
                               connected=True,
                               token=token,
                               connectionInfo={
                                   "token": token,
                                   "email": session["email"],
                                   "first_name": session["first_name"],
                                   "family_name": session["family_name"],
                                   "right": session["right"]
                               }), 200
    return json_result(False)

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

@sat_biblio.route("/users/confirm/<token>", methods=["GET"])
def confirmer_inscription_utilisateur(token):
    email = request.args.get("email")
    user_sess = sm.UserSess(email)
    if user_sess and user_sess.confirmer_token(token):
        connect_user_login(user_sess.user_db)
        return json_result(True, message="Vous êtes connecté.")
    else:
        return json_result(False, message="L'utilisateur n'existe pas")


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
                    link = url_for("sat_biblio.confirmer_inscription_utilisateur", token=token, email=user.email,
                                   _external=True)
                    link_to_resend = ""
                    # print(link)
                    mail_manager.envoyer_mail_demande_inscription_utilisateur(user, link)
                    # connecter_patient_login(patient)
                    # flash(lazy_gettext())
                    return json_result(True, message="Le compte a correctement été créé.",
                                       link_to_resend=link_to_resend)
                    # return render_template("patient/connexion/patient_enregistre.html", inscription_validee=True,
                    #                        mettre_message_succes=True)
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
    # print(session.keys())
    if "email" in session:
        return json_result(True,
                           connectionInfo={"connected": True,
                                           "connectionInfo": {
                                               "email": session["email"],
                                               "first_name": session["first_name"],
                                               "family_name": session["family_name"],
                                               "right": session["right"]
                                           }
                                           })
    else:
        return json_result(False)


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
