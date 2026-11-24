from flask import request, render_template, redirect
from flask_login import login_user

from sat_biblio_server import sat_biblio, UserDB


@sat_biblio.route("/stjoern", methods=["GET", "POST"])
def login_admin():
    if request.method == "GET":
        return render_template("admin/login.html")
    elif request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        user = UserDB.query.filter_by(email=email).first()
        if not user:
            return render_template("admin/login.html", message="Identifiant ou mot de passe incorrect.")
        if not user.verify_password(password):
            return render_template("admin/login.html", message="Identifiant ou mot de passe incorrect.")
        if not login_user(user):
            return render_template("admin/login.html", message="Identifiant ou mot de passe incorrect.")
        return redirect("/admin/")
