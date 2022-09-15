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
        data = request.get_json()
        message = data["message"]
        if "10" != data["theSum"]:
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
