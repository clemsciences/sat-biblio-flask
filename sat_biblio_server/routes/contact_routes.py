"""

"""

from flask import request, session

from sat_biblio_server import sat_biblio, UserDB, json_result
from sat_biblio_server.managers.mail_manager import envoyer_message_contact
from sat_biblio_server.limiter import limiter, PUBLIC_FORM_LIMIT

# Délai minimal entre l'affichage du formulaire et son envoi.
MIN_FILL_SECONDS = 3


@sat_biblio.route("/contact/send-message/", methods=["POST"])
@limiter.limit(PUBLIC_FORM_LIMIT)
def send_email_to_admin():
    """

    :return:
    """
    if request.method == "POST":
        data = request.get_json() or {}
        message = data.get("message", "")
        # Champ piège rempli : c'est un robot. On répond comme si l'envoi avait
        # réussi, pour ne pas lui indiquer qu'il a été détecté.
        if data.get("website"):
            return json_result(True, mistake=False, message="Mail correctly sent")
        # Un humain met plus de quelques secondes à écrire un message.
        try:
            elapsed_seconds = int(data.get("elapsedSeconds"))
        except (TypeError, ValueError):
            elapsed_seconds = 0
        if elapsed_seconds < MIN_FILL_SECONDS or not message.strip():
            return json_result(False, mistake=True, message="")
        if "email" in session:
            current_user = UserDB.query.filter_by(email=session["email"]).first()
            success = envoyer_message_contact(current_user.email, message)
        else:
            if "emailAddress" in data:
                success = envoyer_message_contact(data["emailAddress"], message)
            else:
                success = envoyer_message_contact("", message)

        if success:
            message = "Mail correctly sent"
        else:
            message = "Error while sending email"
        return json_result(success, mistake=False, message=message)
    return json_result(False, mistake=False, message="Wrong method")
