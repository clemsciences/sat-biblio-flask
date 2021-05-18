"""

"""

from flask import request, session

from sat_biblio_server import sat_biblio, UserDB, json_result
from sat_biblio_server.managers.mail_manager import envoyer_message_contact


@sat_biblio.route("/contact/send-message/", methods=["POST"])
def send_email_to_admin():
    """

    :return:
    """
    message = request.get_json()["message"]
    current_user = UserDB.query.filter_by(email=session["email"]).first()
    envoyer_message_contact(current_user.email, message)
    return json_result(True, message="Mail correctly sent")
