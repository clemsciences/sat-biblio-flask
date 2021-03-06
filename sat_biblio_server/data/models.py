"""

"""


__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

import datetime

from sat_biblio_server import AuthorDB, ReferenceBibliographiqueLivreDB, EnregistrementDB, EmpruntLivreDB, UserDB


class Author:

    @staticmethod
    def from_db_to_data(author_db: AuthorDB):
        return dict(
            first_name=author_db.first_name,
            family_name=author_db.family_name,
            id=author_db.id
        )

    @staticmethod
    def from_data_to_db(author):
        author_db = AuthorDB()
        if "first_name" in author:
            author_db.first_name = author["first_name"]
        if "id" in author:
            author_db.id = author["id"]
        if "family_name" in author:
            author_db.family_name = author["family_name"]
        return author_db

    @staticmethod
    def from_id_to_db(id_):
        return AuthorDB.query.filter_by(id=id_).first()

    @staticmethod
    def from_ids_to_db(ids):
        return [Author.from_id_to_db(id_) for id_ in ids]


class ReferenceBibliographiqueLivre:

    @staticmethod
    def from_data_to_db(reference: dict):
        auteurs_db = []
        for auteur in reference["auteurs"]:
            if "value" in auteur:
                author_db = Author.from_id_to_db(auteur["value"])
                if author_db:
                    auteurs_db.append(author_db)
        reference_db = ReferenceBibliographiqueLivreDB(authors=auteurs_db)
        if "id" in reference:
            reference_db.id = reference["id"]
        if "titre" in reference:
            reference_db.titre = reference["titre"]
        if "lieu_edition" in reference:
            reference_db.lieu_edition = reference["lieu_edition"]
        if "editeur" in reference:
            reference_db.editeur = reference["editeur"]
        if "annee" in reference:
            reference_db.annee = reference["annee"]
        if "nb_page" in reference:
            reference_db.nb_page = reference["nb_page"]
        return reference_db

    @staticmethod
    def from_db_to_data(reference: ReferenceBibliographiqueLivreDB):
        return dict(
            id=reference.id,
            authors=[Author.from_db_to_data(author_db) for author_db in reference.authors],
            titre=reference.titre,
            lieu_edition=reference.lieu_edition,
            editeur=reference.editeur,
            annee=reference.annee,
            nb_page=reference.nb_page
        )

    @staticmethod
    def from_id_to_db(id_):
        return ReferenceBibliographiqueLivreDB.query.filter_by(id=id_).first()

    @staticmethod
    def from_ids_to_db(ids):
        return [ReferenceBibliographiqueLivre.from_id_to_db(id_) for id_ in ids]


class Enregistrement:

    @staticmethod
    def from_data_to_db(enregistrement: dict) -> EnregistrementDB:
        date_modification = datetime.datetime.now()
        if "valide" in enregistrement:
            valide = enregistrement["valide"]
        else:
            valide = False
        enregistrement_db = EnregistrementDB(date_modification=date_modification, valide=valide)
        if "id" in enregistrement:
            enregistrement_db.id = enregistrement["id"]
        if "id_reference" in enregistrement:
            enregistrement_db.id_reference = enregistrement["id_reference"]
        if "description" in enregistrement:
            enregistrement_db.description = enregistrement["description"]
        if "cote" in enregistrement:
            enregistrement_db.cote = enregistrement["cote"]
        if "annnee" in enregistrement:
            enregistrement_db.annee = enregistrement["annee"]
        if "nb_exemplaire_supp" in enregistrement:
            enregistrement_db.nb_exemplaire_supp = enregistrement["nb_exemplaire_supp"]
        if "provenance" in enregistrement:
            enregistrement_db.provenance = enregistrement["provenance"]
        if "mots_clef" in enregistrement:
            enregistrement_db.mots_clef = enregistrement["mots_clef"]
        return enregistrement_db

    @staticmethod
    def from_db_to_data(enregistrement_db: EnregistrementDB) -> dict:
        return dict(
            id=enregistrement_db.id,
            reference=ReferenceBibliographiqueLivre.from_db_to_data(enregistrement_db.reference),
            annee=enregistrement_db.annee,  # année d'obtention
            description=enregistrement_db.description,
            cote=enregistrement_db.cote,
            nb_exemplaire_supp=enregistrement_db.nb_exemplaire_supp,
            provenance=enregistrement_db.provenance,
            mots_clef=enregistrement_db.mots_clef,
            date_modification=enregistrement_db.date_modification,
            valide=enregistrement_db.valide)


class EmpruntLivre:
    @staticmethod
    def from_data_to_db(emprunt: dict) -> EmpruntLivreDB:
        return EmpruntLivreDB(id_emprunteur=emprunt["id_emprunteur"],
                              id_enregistrement=emprunt["id_enregistrement"],
                              id_gestionnaire=emprunt["id_gestionnaire"],
                              commentaire=emprunt["commentaire"],
                              emprunte=emprunt["emprunte"],
                              date_emprunt=emprunt["date_emprunt"],
                              date_retour_prevu=emprunt["date_retour_prevu"],
                              date_retour_reel=emprunt["date_retour_reel"],
                              rendu=emprunt["rendu"])

    @staticmethod
    def from_db_to_data(emprunt_db: EmpruntLivreDB):
        return dict(
            id_gestionnaire=emprunt_db.id_gestionnaire,
            gestionnaire=User.from_db_to_data(emprunt_db.gestionnaire),
            id_enregistrement=emprunt_db.id_enregistrement,
            enregistrement=Enregistrement.from_db_to_data(emprunt_db.enregistrement),
            id_emprunteur=emprunt_db.id_emprunteur,
            emprunteur=emprunt_db.emprunteur,
            commentaire=emprunt_db.commentaire,
            emprunte=emprunt_db.emprunte,
            date_emprunt=emprunt_db.date_emprunt,
            date_retour_prevu=emprunt_db.date_retour_prevu,
            date_retour_reel=emprunt_db.date_retour_reel,
            rendu=emprunt_db.rendu
        )


class User:
    @staticmethod
    def from_db_to_data(user_db: UserDB):
        return dict(
            first_name=user_db.first_name,
            family_name=user_db.family_name,
            email=user_db.email,
            right=user_db.right.value,
            id=user_db.id
        )

    @staticmethod
    def from_data_to_db(user: dict):
        return UserDB(first_name=user["first_name"],
                      family_name=user["family_name"],
                      email=user["email"],
                      right=user["right"],
                      id=user["id"])
