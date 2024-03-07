"""

"""


__author__ = ["Clément Besnier <clem@clementbesnier.fr", ]

import logging


def check_user(user):
    return "first_name" in user and \
           "family_name" in user and \
           "email" in user and \
           user["first_name"] and \
           user["family_name"] and \
           user["email"]


def check_author(author):
    return "first_name" in author and \
           "family_name" in author and \
           author["first_name"] and \
           author["family_name"]


def check_borrow(borrow):
    # TODO
    return True


def check_enregistrement(enregistrement):
    return "id_reference" in enregistrement and \
           "cote" in enregistrement and \
           "annee" in enregistrement and \
           "nb_exemplaire_supp" in enregistrement and \
           "provenance" in enregistrement and \
           "aide_a_la_recherche" in enregistrement and \
           enregistrement["id_reference"] > 0 and \
           len(enregistrement["nb_exemplaire_supp"]) == 0 or \
           ((type(enregistrement["nb_exemplaire_supp"]) == str and
             enregistrement["nb_exemplaire_supp"].isdigit()) or
            (type(enregistrement["nb_exemplaire_supp"]) == int))


def check_reference_bibliographique_livre(reference):
    return "auteurs" in reference and \
           "titre" in reference and \
           "lieu_edition" in reference and \
           "editeur" in reference and \
           "annee" in reference and \
           "nb_page" in reference and \
           "description" in reference and \
           reference["auteurs"] and \
           reference["titre"] and \
           reference["lieu_edition"] and \
           reference["editeur"] and \
           reference["description"]
    # and \
    # (type(reference["annee"]) == int or
    #  type(reference["annee"]) == str and
    #  reference["annee"].isdigit()) and \
    # type(reference["nb_page"]) == int


def check_user_connection(user_connection):
    # logging.log(logging.DEBUG, user_connection)
    return "email" in user_connection and \
           "password" in user_connection and \
           user_connection["email"] and \
           user_connection["password"]


def check_emprunt(emprunt):
    return "borrower" in emprunt and \
           "record" in emprunt and \
           "comment" in emprunt and \
           "dateComebackExpected" in emprunt


def check_log_event(log_event):
    return "id" in log_event and \
           "event_type" in log_event and \
           "object_id" in log_event and \
           "event_datetime" in log_event and \
           "event_owner" in log_event and \
           "table_name" in log_event
