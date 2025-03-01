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


def check_enregistrement_complet(enregistrement_avec_reference):
    if "cote" not in enregistrement_avec_reference:
        print("cote is missing")
        return False
    elif "publication_annee" not in enregistrement_avec_reference:
        print("publication_annee is missing")
        return False
    elif "annee_entree" not in enregistrement_avec_reference:
        print("annee_entree is missing")
        return False
    elif "nb_exemplaire_supp" not in enregistrement_avec_reference:
        print("nb_exemplaire_supp is missing")
        return False
    elif "provenance" not in enregistrement_avec_reference:
        print("provenance is missing")
        return False
    elif "aide_a_la_recherche" not in enregistrement_avec_reference:
        print("aide_a_la_recherche is missing")
        return False
    elif "authors" not in enregistrement_avec_reference:
        print("authors is missing")
        return False
    elif "titre" not in enregistrement_avec_reference:
        print("titre is missing")
        return False
    elif "lieu_edition" not in enregistrement_avec_reference:
        print("lieu_edition is missing")
        return False
    elif "editeur" not in enregistrement_avec_reference:
        print("editeur is missing")
        return False
    elif "annee_entree" not in enregistrement_avec_reference:
        print("annee_entree is missing")
        return False
    elif "nb_page" not in enregistrement_avec_reference:
        print("nb_page is missing")
        return False
    elif "reference_description" not in enregistrement_avec_reference:
        print("reference_description is missing")
        return False
    elif not enregistrement_avec_reference["authors"]:
        print("authors is void")
        return False
    elif not enregistrement_avec_reference["titre"]:
        print("titre is void")
        return False
    elif not enregistrement_avec_reference["lieu_edition"]:
        print("lieu_edition is void")
        return False
    elif not enregistrement_avec_reference["editeur"]:
        print("editeur is void")
        return False
    return True



def check_enregistrement(enregistrement):
    return "id_reference" in enregistrement and \
           "cote" in enregistrement and \
           "annee" in enregistrement and \
           "nb_exemplaire_supp" in enregistrement and \
           "provenance" in enregistrement and \
           "aide_a_la_recherche" in enregistrement and \
           enregistrement["id_reference"] > 0


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
           reference["editeur"]


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
