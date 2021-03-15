"""
Only module which uses flask_mail
"""

import logging
import random
from smtplib import SMTPSenderRefused, SMTPRecipientsRefused, SMTPDataError, SMTPServerDisconnected
from typing import Union

from flask import render_template
from flask_mail import Message
from flask_babel import lazy_gettext

from sat_biblio_server import mail
from sat_biblio_server.database.users import UserDB
from sat_biblio_server.config.development import Config

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


SENDER = "admin@skilvit.fr"


def send_email(msg: Message, recipient_email_address: str):
    """
    Send email with logs in case it fails

    :param msg:
    :param recipient_email_address:
    :return:
    """
    try:
        mail.send(msg)
        return True
    except SMTPSenderRefused:
        logging.error("Email could not be sent due to refused sender " + SENDER)
    except SMTPRecipientsRefused:
        logging.error("Email could not be sent due to refused recipient " + recipient_email_address)
    except SMTPDataError:
        logging.error("Email could not be sent due to data error " + recipient_email_address)
    except SMTPServerDisconnected:
        logging.error("Email could not be sent due to error ("+SENDER+", "+recipient_email_address+")")
    return False


def send_email_new_password(recipient: str, nouveau_mot_de_passe: str):
    """

    :param recipient:
    :param nouveau_mot_de_passe:
    :return:
    """
    msg = Message("Réinitialisation du mot de passe de SatBiblio",
                  sender=Config.EMAIL_HOST_USER,
                  html=render_template(recipient=recipient,
                                       nouveau_mot_de_passe=nouveau_mot_de_passe,
                                       expediteur=Config.EMAIL_HOST_USER))
    send_email(msg, recipient)


def generer_lien_inscription():
    return random.sample("azertyuiopqsdfghjklmwxcvbn0123456789", 30)


def envoyer_mail_demande_inscription_utilisateur(user: Union[UserDB], link):
    msg = Message(lazy_gettext("SAT biblio - validation de l'inscription"), sender=SENDER,
                  html=render_template("mails/demande_confirmation_utilisateur.html", user=user,
                                       link_to_validate="", link_to_dismiss="", link=link))
    msg.add_recipient((user.first_name + " " + user.family_name, user.email))
    return send_email(msg, user.email)


def envoyer_mail_attente_inscription_praticien(user: Union[UserDB], token):
    msg = Message(lazy_gettext("Skilvit - attente validation inscription"), sender=SENDER,
                  html=render_template("mails/attente_validation_praticien.html", user=user))
    msg.add_recipient((user.first_name + " " + user.family_name, user.email))
    return send_email(msg, user.email)


def envoyer_message_contact(email_address: str, content: str):
    # Send to contact
    msg1 = Message(subject=lazy_gettext("Message envoyé à Skilvit"), sender=SENDER,
                   html=render_template("mails/message_contact.html", corps=content))
    msg1.add_recipient((email_address, email_address))
    res = send_email(msg1, email_address)

    # Send to admin of the website
    msg2 = Message(subject=lazy_gettext("Message reçu d'un curieux"), sender=SENDER,
                   html=render_template("mails/message_contact_admin.html", destinataire=email_address, corps=content))
    msg2.add_recipient((SENDER, SENDER))
    return send_email(msg2, SENDER) and res


