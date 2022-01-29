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
    if request.method == "POST":
        message = request.get_json()["message"]
        if "10" != request.get_json()["theSum"]:
            return json_result(False, mistake=True, message="")
        current_user = UserDB.query.filter_by(email=session["email"]).first()
        envoyer_message_contact(current_user.email, message)
        return json_result(True, mistake=False, message="Mail correctly sent")
    else:
        return json_result(False, mistake=False, message="Wrong method")
