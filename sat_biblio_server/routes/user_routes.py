"""

"""
import json

from flask import url_for, session, request
from flask_login import login_user, logout_user
from sqlalchemy import or_
from werkzeug.security import generate_password_hash

from sat_biblio_server import sat_biblio
from sat_biblio_server.managers import mail_manager
import sat_biblio_server.database as dbm
import sat_biblio_server.sessions.session_manager as sm
import sat_biblio_server.data.validation as dv
from sat_biblio_server.utils import json_result


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region connexion


def connect_user_login(user):
    if login_user(user):
        session["email"] = user.email
        session["first_name"] = user.first_name
        session["family_name"] = user.family_name


@sat_biblio.route("/users/connect", methods=["POST"])
def connect_user():
    if "email" in session:
        return json_result(True, {
            "connectionInfo": {
                "email": session["email"],
                "first_name": session["first_name"],
                "family_name": session["family_name"]
            }
        })
    else:
        data = request.get_json()
        if dv.check_user_connection(data):
            user = dbm.UserDB.query.filter_by(email=data["email"]).first()
            if user is None:
                print("identification a échoué")
                return json_result(False, message="L'adresse email ou le mot de passe est incorrect.")

            if not user.verify_password(data["password"]):
                print("mauvais mot de passe")
                return json_result(False, message="L'adresse email ou le mot de passe est incorrect.")
            if not user.confirmed:
                print("utilisateur non confirmé")
                return json_result(False, message="L'utilisateur n'est pas confirmé")
            connect_user_login(user)
            print("bien connecté")
            return json_result(True, message="Vous êtes bien connecté.",
                               connectionInfo={"connected": True,
                                               "connectionInfo": {
                                                   "email": session["email"],
                                                   "first_name": session["first_name"],
                                                   "family_name": session["family_name"]
                                               }})
    return json_result(False)


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
def deconnecter_patient():
    if logout_user():
        if "email" in session:
            del session["email"]
        if "first_name" in session:
            del session["first_name"]
        if "family_name" in session:
            del session["family_name"]
    # session.pop("pseudo_patient", None)
    # session.modified = True
    return json_result(True)


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
                                               "family_name": session["family_name"]
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


# endregion
