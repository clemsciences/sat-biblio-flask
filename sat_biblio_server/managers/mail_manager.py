"""
Only module which uses flask_mail
"""

import logging
import random
from smtplib import SMTPSenderRefused, SMTPRecipientsRefused, SMTPDataError, SMTPServerDisconnected, SMTPAuthenticationError
from typing import Union

from flask import render_template
from flask_mail import Message
from flask_babel import lazy_gettext

from sat_biblio_server import mail, ReferenceBibliographiqueLivre2023DB, EmpruntLivre2023DB
from sat_biblio_server.database.users import UserDB
from sat_biblio_server.config.development import Config

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


SENDER = "sarcheot@gmail.com"


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
    except SMTPAuthenticationError:
        logging.error(f"Email could not be sent because of invalid credentials: {recipient_email_address}")
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
    msg = Message("Réinitialisation du mot de passe de SAT biblio",
                  sender=Config.MAIL_DEFAULT_SENDER,
                  html=render_template("mails/nouveau_mot_de_passe.html", recipient=recipient,
                                       nouveau_mot_de_passe=nouveau_mot_de_passe,
                                       expediteur=Config.MAIL_DEFAULT_SENDER))
    msg.add_recipient(recipient)
    return send_email(msg, recipient)


def generer_lien_inscription():
    return random.sample("azertyuiopqsdfghjklmwxcvbn0123456789", 30)


def envoyer_mail_demande_inscription_utilisateur(user: Union[UserDB], link):
    msg = Message(lazy_gettext("SAT biblio - validation de l'inscription"), sender=SENDER,
                  html=render_template("mails/demande_confirmation_utilisateur.html", user=user,
                                       link_to_validate="", link_to_dismiss="", link=link))
    msg.add_recipient((user.first_name + " " + user.family_name, user.email))
    return send_email(msg, user.email)


def envoyer_message_contact(user_email_address: str, message: str) -> bool:
    # Send to contact
    if user_email_address:
        msg1 = Message(subject="Copie du message envoyé à SAT biblio", sender=SENDER,
                       html=render_template("mails/message_contact.html", message=message))
        msg1.add_recipient(user_email_address)
        # mail.send(msg1)
        res = send_email(msg1, user_email_address)
        if not res:
            return False

    # Send to admin of the website
    msg2 = Message(subject="Message reçu d'un utilisateur de SAT biblio", sender=SENDER,
                   html=render_template("mails/message_contact.html", destinataire=user_email_address, message=message))
    msg2.add_recipient(SENDER)
    return send_email(msg2, user_email_address)


def send_new_borrowing_email(user_email_address: Union[UserDB], reference: ReferenceBibliographiqueLivre2023DB, borrowing: EmpruntLivre2023DB):
    msg = Message(lazy_gettext(f"Nouvel emprunt à la BHT : \"{reference.titre}\""), sender=SENDER,
                  html=render_template("mails/new_borrowing.html", user=user_email_address,
                                       reference=reference,
                                       first_name=user_email_address.first_name,
                                       family_name=user_email_address.family_name,
                                       title= reference.titre,
                                       borrowing_date=borrowing.date_emprunt.strftime("%d/%m/%Y"),
                                       end_borrowing_date=borrowing.date_retour_prevu.strftime("%d/%m/%Y")))
    msg.add_recipient((user_email_address.first_name + " " + user_email_address.family_name, user_email_address.email))
    return send_email(msg, user_email_address.email)


def send_late_borrowing(user: Union[UserDB], reference: ReferenceBibliographiqueLivre2023DB, borrowing: EmpruntLivre2023DB):
    msg = Message(lazy_gettext(""), sender=SENDER,
                  html=render_template("mails/borrowing_late.html"))
    return send_email(msg, user.email)


def send_borrowing_soon_finished(user: Union[UserDB], reference: ReferenceBibliographiqueLivre2023DB, borrowing: EmpruntLivre2023DB):
    msg = Message(lazy_gettext(""), sender=SENDER,
                  html=render_template("mails/borrowing_soon_finished.html.html"))
    return send_email(msg, user.email)
