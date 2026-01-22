"""

"""

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

import abc
import datetime
import logging
from typing import Union, List, Dict, Optional, Tuple

from sat_biblio_server import Author2023DB, ReferenceBibliographiqueLivre2023DB, Enregistrement2023DB, \
    EmpruntLivre2023DB, \
    UserDB, LogEventDB, db, ImportDB, HelperAuthorBook2023
from sqlalchemy import and_, join, text

from sat_biblio_server.utils import DateHeureUtils


class IoData(abc.ABC):

    @abc.abstractmethod
    def from_db_to_data(self, db_object):
        pass

    @abc.abstractmethod
    def from_data_to_db(self, data_object):
        pass

    @abc.abstractmethod
    def from_data_to_csv_row(self, data):
        pass

    @abc.abstractmethod
    def get_column_names(self):
        pass

    @abc.abstractmethod
    def from_id_to_db(self, id_: int):
        pass

    @abc.abstractmethod
    def from_ids_to_db(self, ids: List[int]):
        pass



class Author2023:

    def __init__(self, **kwargs):
        self.first_name = kwargs.get("first_name", "")
        self.family_name = kwargs.get("family_name", "")
        self.ark_name = kwargs.get("ark_name", "")

    def __str__(self):
        return f"{self.first_name} {self.family_name}"

    def __repr__(self):
        return f"<Author> {self}"

    @staticmethod
    def from_db_to_data(author_db: Author2023DB):
        if author_db:
            return dict(
                first_name=author_db.first_name,
                family_name=author_db.family_name,
                id=author_db.id,
                valide=author_db.valide,
                ark_name=author_db.ark_name
            )
        else:
            return {}

    @staticmethod
    def from_data_to_db(author):
        author_db = Author2023DB()
        if "first_name" in author:
            author_db.first_name = author["first_name"]
        if "id" in author:
            author_db.id = author["id"]
        if "family_name" in author:
            author_db.family_name = author["family_name"]
        if "valide" in author:
            author_db.valide = author["valide"]
        if "ark_name" in author:
            author_db.ark_name = author["ark_name"]
        else:
            author_db.valide = False
        return author_db

    # region CSV & Excel
    @staticmethod
    def from_data_to_csv_row(data: dict):
        return f"{data.get('family_name', '')} ({data.get('first_name', '')})"

    @staticmethod
    def get_column_names():
        return ["Auteurs"]
    # endregion

    @staticmethod
    def from_id_to_db(id_):
        return Author2023DB.query.filter_by(id=id_).first()

    @staticmethod
    def from_ids_to_db(ids):
        return [Author2023.from_id_to_db(id_) for id_ in ids]

    @staticmethod
    def get_authors_by_ref(id_ref, n_page, size, sort_by):
        """
        select * from authors where


        :param id_ref:
        :param n_page:
        :param size:
        :param sort_by:
        :return:
        """
        the_query = Author2023DB.query
        the_query = the_query.join(ReferenceBibliographiqueLivre2023DB.authors)
        the_query = the_query.filter(ReferenceBibliographiqueLivre2023DB.id == id_ref)
        return [dict(type="author", description=str(author), id=author.id)
                for author in the_query.paginate(page=n_page, per_page=size).items]

    @staticmethod
    def get_authors_by_ref_count(id_ref):
        """
        select * from authors where

        :param id_ref:
        :return:
        """
        the_query = Author2023DB.query
        the_query = the_query.join(ReferenceBibliographiqueLivre2023DB.authors)
        the_query = the_query.filter(ReferenceBibliographiqueLivre2023DB.id == id_ref)
        return the_query.count()

    @staticmethod
    def get_authors_by_record(id_record, n_page, size, sort_by):
        """
        select * from authors where


        :param id_record:
        :param n_page:
        :param size:
        :param sort_by:
        :return:
        """
        logging.warning(id_record)
        refs_db = ReferenceBibliographiqueLivre2023DB.query.filter(
            and_(Enregistrement2023DB.reference,
                 Enregistrement2023DB.id == id_record)).all()
        logging.warning(refs_db)
        refs = [ReferenceBibliographiqueLivre2023.from_db_to_data(ref) for ref in refs_db]
        logging.warning(refs)
        if refs:
            the_query = Author2023DB.query.filter(
                and_(ReferenceBibliographiqueLivre2023DB.authors,
                     ReferenceBibliographiqueLivre2023DB.id == refs[0]["id"]))
            return [dict(type="author", description=str(author), id=author.id)
                    for author in the_query.paginate(page=n_page, per_page=size).items]
        else:
            return []
        # the_query = AuthorDB.query
        # the_query = the_query.join(ReferenceBibliographiqueLivreDB.authors)
        # the_query = the_query.join(EnregistrementDB.reference)
        # the_query = the_query.filter(EnregistrementDB.id == id_record)

    @staticmethod
    def get_authors_by_record_count(id_record):
        """
        select * from authors where


        :param id_record:
        :return:
        """
        refs_db = ReferenceBibliographiqueLivre2023DB.query.filter(
            and_(Enregistrement2023DB.reference,
                 Enregistrement2023DB.id == id_record)).all()
        logging.warning(refs_db)
        refs = [ReferenceBibliographiqueLivre2023.from_db_to_data(ref) for ref in refs_db]
        logging.warning(refs)
        if refs:
            the_query = Author2023DB.query.filter(
                and_(ReferenceBibliographiqueLivre2023DB.authors,
                     ReferenceBibliographiqueLivre2023DB.id == refs[0]["id"]))
            return the_query.count()
        else:
            return 0

        # the_query = AuthorDB.query
        # the_query = the_query.join(ReferenceBibliographiqueLivreDB.authors)
        # the_query = the_query.join(EnregistrementDB.reference)
        # the_query = the_query.filter(EnregistrementDB.id == id_record)
        # return the_query.count()

    @staticmethod
    def get_authors_without_ref(n_page, size, sort_by):
        the_query = Author2023DB.query.filter(Author2023DB.id.not_in(ReferenceBibliographiqueLivre2023DB.authors))
        return [dict(type="author", description=str(author), id=author.id)
                for author in the_query.paginate(page=n_page, per_page=size).items]


class ReferenceBibliographiqueLivre2023:

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"<ReferenceBibliographiqueLivre> {self.title}"

    @staticmethod
    def from_data_to_db(reference: dict):
        auteurs_db = []
        for auteur in reference["auteurs"]:
            if type(auteur) == dict:
                if "value" in auteur:
                    author_db = Author2023.from_id_to_db(auteur["value"])
                    if author_db:
                        auteurs_db.append(author_db)
            elif isinstance(auteur, Author2023):
                print(auteur)

        reference_db = ReferenceBibliographiqueLivre2023DB()
        reference_db.authors = auteurs_db
        if "id" in reference:
            reference_db.id = reference["id"]
        if "titre" in reference:
            reference_db.titre = reference["titre"]
        if "lieu_edition" in reference and reference["lieu_edition"]:
            reference_db.lieu_edition = reference["lieu_edition"]
        else:
            reference_db.lieu_edition = "s. l."
        if "editeur" in reference and reference["editeur"]:
            reference_db.editeur = reference["editeur"]
        else:
            reference_db.editeur = "s. ed."
        if "publication_annee" in reference and reference["publication_annee"]:
            reference_db.annee = reference["publication_annee"]
        elif "annee" in reference and reference["annee"]:
            reference_db.annee = reference["annee"]
        else:
            reference_db.annee = "s. d."
        if "nb_page" in reference:
            reference_db.nb_page = reference["nb_page"]
        # if "valide" in reference:
        #     reference_db.valide = reference["valide"]
        # else:
        #     reference_db.valide = False
        if "description" in reference:
            reference_db.description = reference["description"]
        if "ark_name" in reference:
            reference_db.ark_name = reference["ark_name"]

        return reference_db

    @staticmethod
    def from_db_to_data(reference_db: ReferenceBibliographiqueLivre2023DB):
        if reference_db:
            date_derniere_modification_str = ""
            if reference_db.date_derniere_modification:
                date_derniere_modification_str = DateHeureUtils.date_to_vue_str(
                    reference_db.date_derniere_modification)
            return dict(
                id=reference_db.id,
                authors=[Author2023.from_db_to_data(author_db) for author_db in reference_db.authors],
                authors_form=reference_db.authors_form,
                selectedAuthors=[Author2023.from_db_to_data(author_db) for author_db in reference_db.authors],
                titre=reference_db.titre,
                lieu_edition=reference_db.lieu_edition,
                editeur=reference_db.editeur,
                annee=reference_db.annee,
                publication_annee=reference_db.annee,
                nb_page=reference_db.nb_page,
                ark_name=reference_db.ark_name,
                date_derniere_modification=date_derniere_modification_str,
                # region meta
                # valide=reference.valide,

                description=reference_db.description
                # endregion
            )
        else:
            return {}

    # region CSV & Excel
    @staticmethod
    def from_data_to_csv_row(data: dict) -> List:
        return [
            " ; ".join([Author2023.from_data_to_csv_row(author_data) for author_data in data.get("authors", [])]),
            data.get("titre", ""),
            data.get("lieu_edition", "s. l."),
            data.get("editeur", "s. e."),
            data.get("annee", "s. a."),
            data.get("nb_page", ""),
            # region meta
            data.get("description", ""),
            data.get("date_derniere_modification", "")
            # endregion
        ]

    @staticmethod
    def get_column_names():
        return Author2023.get_column_names() + \
            ["Titre", "Lieu d'édition", "Editeur", "Année d'édition",
             "Nombre de pages", "Description"]
    # endregion

    @staticmethod
    def from_id_to_db(id_):
        return ReferenceBibliographiqueLivre2023DB.query.filter_by(id=id_).first()

    @staticmethod
    def from_ids_to_db(ids):
        return [ReferenceBibliographiqueLivre2023.from_id_to_db(id_) for id_ in ids]

    @staticmethod
    def get_references_by_author(id_author, n_page, size, sort_by):
        """
        >>> ReferenceBibliographiqueLivre2023.get_references_by_author(12, 0, 0, 0)

        :param id_author:
        :param n_page:
        :param size:
        :param sort_by:
        :return:
        """
        with db.engine.connect() as connection:
            res = connection.execute(text(f"SELECT * FROM {ReferenceBibliographiqueLivre2023DB.__tablename__} "
                                    f"WHERE id IN "
                                    f"(SELECT id_reference_biblio_livre FROM {HelperAuthorBook2023.__tablename__} "
                                    f"WHERE id_author = {id_author}) LIMIT {size} OFFSET {(n_page - 1) * size}"))
            return [dict(type="reference", description=str(ref_db["titre"])+", "+ref_db["editeur"], id=ref_db["id"])
                    for ref_db in res.mappings()]

    @staticmethod
    def get_references_by_author_count(id_author):
        """
        >>> ReferenceBibliographiqueLivre2023.get_references_by_author(12, 0, 0, 0)

        :param id_author:
        :return:
        """
        with db.engine.connect() as connection:
            res = connection.execute(text(f"SELECT COUNT(*) FROM {ReferenceBibliographiqueLivre2023DB.__tablename__} "
                                    f"WHERE id IN "
                                    f"(SELECT id_reference_biblio_livre FROM {HelperAuthorBook2023.__tablename__} "
                                    f"WHERE id_author = {id_author} )"))
            for i in res:
                return i[0]

    @staticmethod
    def get_references_by_record(id_record, n_page, size, sort_by):
        """

        :param id_record:
        :param n_page:
        :param size:
        :param sort_by:
        :return:
        """
        the_query = ReferenceBibliographiqueLivre2023DB.query
        the_query = the_query.join(Enregistrement2023DB.reference)
        the_query = the_query.filter(Enregistrement2023DB.id == id_record)
        return [dict(type="reference", description=f"{ref_db.titre}, {ref_db.editeur}", id=ref_db.id)
                for ref_db in the_query.paginate(page=n_page, per_page=size).items]

    @staticmethod
    def get_references_by_record_count(id_record):
        """

        :param id_record:
        :return:
        """
        the_query = ReferenceBibliographiqueLivre2023DB.query
        the_query = the_query.join(Enregistrement2023DB.reference)
        the_query = the_query.filter(Enregistrement2023DB.id == id_record)
        return the_query.count()


class Enregistrement2023:

    def __init__(self):
        self.cote = ""

    @staticmethod
    def from_data_to_db(enregistrement: dict) -> Enregistrement2023DB:
        date_modification = datetime.datetime.now()
        if "valide" in enregistrement:
            valide = enregistrement["valide"]
        else:
            valide = False
        enregistrement_db = Enregistrement2023DB()
        enregistrement_db.date_derniere_modification = date_modification
        enregistrement_db.valide = valide
        if "id" in enregistrement:
            enregistrement_db.id = enregistrement["id"]
        if "id_reference" in enregistrement:
            enregistrement_db.id_reference = enregistrement["id_reference"]
        if "cote" in enregistrement:
            enregistrement_db.cote = enregistrement["cote"]
        if "annee_obtention" in enregistrement and enregistrement["annee_obtention"]:
            enregistrement_db.annee_obtention = enregistrement["annee_obtention"]
        elif "annee" in enregistrement and enregistrement["annee"]:
            enregistrement_db.annee_obtention = enregistrement["annee"]
        else:
            enregistrement_db.annee_obtention = ""
        # if "nb_exemplaire_supp" in enregistrement:
        #     enregistrement_db.nb_exemplaire_supp = enregistrement["nb_exemplaire_supp"]
        if "provenance" in enregistrement:
            enregistrement_db.provenance = enregistrement["provenance"]
        # if "mots_clef" in enregistrement:
        #     enregistrement_db.mots_clef = enregistrement["mots_clef"]
        if "commentaire" in enregistrement:
            enregistrement_db.commentaire = enregistrement["commentaire"]
        if "observations" in enregistrement:
            enregistrement_db.observations = enregistrement["observations"]
        if "aide_a_la_recherche" in enregistrement:
            enregistrement_db.aide_a_la_recherche = enregistrement["aide_a_la_recherche"]
        if "ark_name" in enregistrement:
            enregistrement_db.ark_name = enregistrement["ark_name"]
        # region meta
        # if "row" in enregistrement:
        #     enregistrement_db.row = enregistrement["row"]
        if "valide" in enregistrement:
            enregistrement_db.valide = enregistrement["valide"]
        if "origin" in enregistrement:
            enregistrement_db.origin = enregistrement["origin"]
        if "date_desherbe" in enregistrement:
            enregistrement_db.date_desherbe = enregistrement["date_desherbe"]
        # endregion
        return enregistrement_db

    @staticmethod
    def from_db_to_data(enregistrement_db: Enregistrement2023DB) -> dict:
        if enregistrement_db:
            annee_obtention = enregistrement_db.annee_obtention
            if type(annee_obtention) == datetime.date or type(annee_obtention) == datetime.datetime:
                annee_obtention = f"{annee_obtention.year}"
            date_derniere_modification = enregistrement_db.date_derniere_modification
            if type(date_derniere_modification) == datetime.date or type(date_derniere_modification) == datetime.datetime:
                date_derniere_modification = date_derniere_modification.isoformat()
            date_desherbe = enregistrement_db.date_desherbe
            if type(date_desherbe) == datetime.date or  type(date_desherbe) == datetime.datetime:
                date_desherbe = date_desherbe.isoformat()

            date_derniere_modification_str = ""
            if enregistrement_db.date_derniere_modification:
                date_derniere_modification_str = DateHeureUtils.date_to_vue_str(enregistrement_db.date_derniere_modification)
            
            return dict(
                id=enregistrement_db.id,
                reference=ReferenceBibliographiqueLivre2023.from_db_to_data(enregistrement_db.reference),
                annee_obtention=annee_obtention,  # année d'obtention
                commentaire=enregistrement_db.commentaire,
                cote=enregistrement_db.cote,
                # nb_exemplaire_supp=enregistrement_db.nb_exemplaire_supp,
                provenance=enregistrement_db.provenance,
                aide_a_la_recherche=enregistrement_db.aide_a_la_recherche,
                observations=enregistrement_db.observations,
                ark_name=enregistrement_db.ark_name,
                # region meta
                date_desherbe=date_desherbe,
                date_derniere_modification=date_derniere_modification_str,
                valide=enregistrement_db.valide,
                origin=enregistrement_db.origin,
                row=enregistrement_db.row,
                # endregion
            )
        else:
            return {}

    # region CSV & Excel
    @staticmethod
    def from_data_to_csv_row(data: dict):
        return ReferenceBibliographiqueLivre2023.from_data_to_csv_row(data.get("reference")) + \
            [
                data.get("cote", ""),
                data.get("observations", ""),
                data.get("annee_obtention", ""),
                data.get("date_desherbe", ""),
                data.get("commentaire", ""),
                data.get("nb_exemplaire_supp", ""),
                data.get("provenance", ""),
                data.get("origin", ""),
                data.get("aide_a_la_recherche", ""),

                # data.get("date_modification", ""),
                data.get("row", "")
               ]

    # @staticmethod
    # def get_column_names():
    #     return ReferenceBibliographiqueLivre2023.get_column_names() + \
    #         ["Cote", "Observations", "Ouvrages supprimés en 2022", "Provenance et date d'entrée", "Description", "Nombre d'exemplaire supplémentaire",
    #          "Aide à la recherche", "Observations", "Ligne"]
    # endregion

    @staticmethod
    def get_records_by_author(id_author, n_page, size, sort_by):
        """

        :param id_author:
        :param n_page:
        :param size:
        :param sort_by:
        :return:
        """
        request = f"SELECT * FROM {Enregistrement2023DB.__tablename__} " \
                  f"WHERE id_reference IN " \
                  f"(SELECT id_reference_biblio_livre FROM {HelperAuthorBook2023.__tablename__} " \
                  f"WHERE id_author = {id_author}) LIMIT {size} OFFSET {(n_page-1)*size} "
        with db.engine.connect() as connection:
            res = connection.execute(text(request))
            return [dict(type="record", description=str(rec_db["cote"]), id=rec_db["id"])
                    for rec_db in res.mappings()]

    @staticmethod
    def get_records_by_author_count(id_author):
        """

        :param id_author:
        :return:
        """
        with db.engine.connect() as connection:
            res = connection.execute(text(f"SELECT COUNT(*) FROM {Enregistrement2023DB.__tablename__} "
                          f"WHERE id_reference IN "
                          f"(SELECT id_reference_biblio_livre FROM {HelperAuthorBook2023.__tablename__} "
                          f"WHERE id_author = {id_author} )"))
            for i in res:
                return i[0]

    @staticmethod
    def get_records_by_ref(id_ref, n_page, size, sort_by):
        the_query = Enregistrement2023DB.query
        the_query = the_query.join(Enregistrement2023DB.reference)
        the_query = the_query.filter(ReferenceBibliographiqueLivre2023DB.id == id_ref)
        return [dict(type="record", description=str(rec_db), id=rec_db.id)
                for rec_db in the_query.paginate(page=n_page, per_page=size).items]

    @staticmethod
    def get_records_by_ref_count(id_ref):
        the_query = Enregistrement2023DB.query
        the_query = the_query.join(Enregistrement2023DB.reference)
        the_query = the_query.filter(ReferenceBibliographiqueLivre2023DB.id == id_ref)
        return the_query.count()


class EnregistrementComplet2023:

    def __init__(self):
        self.cote = ""

    @staticmethod
    def from_data_to_db(enregistrement_complet: dict) -> Tuple[ReferenceBibliographiqueLivre2023DB, Enregistrement2023DB]:
        reference_db = ReferenceBibliographiqueLivre2023DB()
        enregistrement_db = Enregistrement2023DB()

        # region update timestamp
        date_modification = datetime.datetime.now()
        reference_db.date_derniere_modification = date_modification
        enregistrement_db.date_derniere_modification = date_modification
        # endregion

        # region valid
        enregistrement_db.valide = True
        # endregion

        # region ids
        if "id" in enregistrement_complet:
            enregistrement_db.id = enregistrement_complet["id"]
        if "id_reference" in enregistrement_complet:
            enregistrement_db.id_reference = enregistrement_complet["id_reference"]
        # endregion

        # region authors
        auteurs_db = []
        for auteur in enregistrement_complet["authors"]:
            if type(auteur) == dict:
                if "value" in auteur:
                    author_db = Author2023.from_id_to_db(auteur["value"])
                    if author_db:
                        auteurs_db.append(author_db)
            elif isinstance(auteur, Author2023):
                print(auteur)
        reference_db.authors = auteurs_db
        # endregion

        # region reference
        if "authors_form" in enregistrement_complet:
            reference_db.authors_form = enregistrement_complet["authors_form"]
        if "titre" in enregistrement_complet:
            reference_db.titre = enregistrement_complet["titre"]
        if "lieu_edition" in enregistrement_complet and enregistrement_complet["lieu_edition"]:
            reference_db.lieu_edition = enregistrement_complet["lieu_edition"]
        else:
            reference_db.lieu_edition = "s. l."
        if "editeur" in enregistrement_complet and enregistrement_complet["editeur"]:
            reference_db.editeur = enregistrement_complet["editeur"]
        else:
            reference_db.editeur = "s. ed."
        if "publication_annee" in enregistrement_complet and enregistrement_complet["publication_annee"]:
            reference_db.annee = enregistrement_complet["publication_annee"]
        elif "annee" in enregistrement_complet and enregistrement_complet["annee"]:
            reference_db.annee = enregistrement_complet["annee"]
        else:
            reference_db.annee = "s. d."
        if "nb_page" in enregistrement_complet:
            reference_db.nb_page = enregistrement_complet["nb_page"]
        # if "valide" in reference:
        #     reference_db.valide = reference["valide"]
        # else:
        #     reference_db.valide = False
        if "reference_description" in enregistrement_complet:
            reference_db.description = enregistrement_complet["reference_description"]
        if "reference_ark_name" in enregistrement_complet:
            reference_db.ark_name = enregistrement_complet["reference_ark_name"]
        # endregion

        # region enregistrement
        if "cote" in enregistrement_complet:
            enregistrement_db.cote = enregistrement_complet["cote"]
        if "annee_entree" in enregistrement_complet and enregistrement_complet["annee_entree"]:
            enregistrement_db.annee_obtention = enregistrement_complet["annee_entree"]
        elif "annee_obtention" in enregistrement_complet and enregistrement_complet["annee_obtention"]:
            enregistrement_db.annee_obtention = enregistrement_complet["annee_obtention"]
        else:
            enregistrement_db.annee_obtention = ""
        # if "nb_exemplaire_supp" in enregistrement:
        #     enregistrement_db.nb_exemplaire_supp = enregistrement["nb_exemplaire_supp"]
        if "provenance" in enregistrement_complet:
            enregistrement_db.provenance = enregistrement_complet["provenance"]
        # if "mots_clef" in enregistrement:
        #     enregistrement_db.mots_clef = enregistrement["mots_clef"]
        if "commentaire" in enregistrement_complet:
            enregistrement_db.commentaire = enregistrement_complet["commentaire"]
        if "observations" in enregistrement_complet:
            enregistrement_db.observations = enregistrement_complet["observations"]
        if "aide_a_la_recherche" in enregistrement_complet:
            enregistrement_db.aide_a_la_recherche = enregistrement_complet["aide_a_la_recherche"]
        if "record_ark_name" in enregistrement_complet:
            enregistrement_db.ark_name = enregistrement_complet["record_ark_name"]
        # endregion

        # region meta
        # if "row" in enregistrement:
        #     enregistrement_db.row = enregistrement["row"]
        if "valide" in enregistrement_complet:
            enregistrement_db.valide = enregistrement_complet["valide"]
        if "origin" in enregistrement_complet:
            enregistrement_db.origin = enregistrement_complet["origin"]
        if "date_desherbe" in enregistrement_complet:
            enregistrement_db.date_desherbe = enregistrement_complet["date_desherbe"]
        # endregion

        return reference_db, enregistrement_db

    @staticmethod
    def from_db_to_data(reference_db: ReferenceBibliographiqueLivre2023DB, enregistrement_db: Enregistrement2023DB) -> dict:
        if enregistrement_db and reference_db:
            annee_obtention = enregistrement_db.annee_obtention
            if type(annee_obtention) == datetime.date or type(annee_obtention) == datetime.datetime:
                annee_obtention = f"{annee_obtention.year}"
            date_derniere_modification = enregistrement_db.date_derniere_modification
            if type(date_derniere_modification) == datetime.date or type(
                    date_derniere_modification) == datetime.datetime:
                date_derniere_modification = date_derniere_modification.isoformat()
            date_desherbe = enregistrement_db.date_desherbe
            if type(date_desherbe) == datetime.date or type(date_desherbe) == datetime.datetime:
                date_desherbe = date_desherbe.isoformat()
            return dict(
                id=enregistrement_db.id,
                annee_entree=annee_obtention,  # année d'obtention
                commentaire=enregistrement_db.commentaire,
                cote=enregistrement_db.cote,
                # nb_exemplaire_supp=enregistrement_db.nb_exemplaire_supp,
                provenance=enregistrement_db.provenance,
                aide_a_la_recherche=enregistrement_db.aide_a_la_recherche,
                observations=enregistrement_db.observations,
                record_ark_name=enregistrement_db.ark_name,
                # region meta
                date_desherbe=date_desherbe,
                date_derniere_modification=date_derniere_modification,
                valide=enregistrement_db.valide,
                origin=enregistrement_db.origin,
                row=enregistrement_db.row,
                # endregion
                reference=ReferenceBibliographiqueLivre2023.from_db_to_data(enregistrement_db.reference),
                authors_form=reference_db.authors_form,
                titre=reference_db.titre,
                lieu_edition=reference_db.lieu_edition,
                editeur=reference_db.editeur,
                publication_annee=reference_db.annee,
                nb_page=reference_db.nb_page,
                reference_description=reference_db.description,
                reference_ark_name=reference_db.ark_name,
            )
        else:
            return {}

    # region CSV & Excel
    # @staticmethod
    # def from_data_to_csv_row(data: dict):
    #     return ReferenceBibliographiqueLivre2023.from_data_to_csv_row(data.get("reference")) + \
    #         [
    #             data.get("cote", ""),
    #             data.get("observations", ""),
    #             data.get("annee_obtention", ""),
    #             data.get("date_desherbe", ""),
    #             data.get("commentaire", ""),
    #             data.get("nb_exemplaire_supp", ""),
    #             data.get("provenance", ""),
    #             data.get("origin", ""),
    #             data.get("aide_a_la_recherche", ""),
    #
    #             # data.get("date_modification", ""),
    #             data.get("row", "")
    #            ]

    # @staticmethod
    # def get_column_names():
    #     return ReferenceBibliographiqueLivre2023.get_column_names() + \
    #         ["Cote", "Observations", "Ouvrages supprimés en 2022", "Provenance et date d'entrée", "Description", "Nombre d'exemplaire supplémentaire",
    #          "Aide à la recherche", "Observations", "Ligne"]
    # endregion

    @staticmethod
    def get_records_by_author(id_author, n_page, size, sort_by):
        """

        :param id_author:
        :param n_page:
        :param size:
        :param sort_by:
        :return:
        """
        request = f"SELECT * FROM {Enregistrement2023DB.__tablename__} " \
                  f"WHERE id_reference IN " \
                  f"(SELECT id_reference_biblio_livre FROM {HelperAuthorBook2023.__tablename__} " \
                  f"WHERE id_author = {id_author}) LIMIT {size} OFFSET {(n_page - 1) * size} "
        with db.engine.connect() as connection:
            res = connection.execute(text(request))
            return [dict(type="record", description=str(rec_db["cote"]), id=rec_db["id"])
                    for rec_db in res.mappings()]

    @staticmethod
    def get_records_by_author_count(id_author):
        """

        :param id_author:
        :return:
        """
        with db.engine.connect() as connection:
            res = connection.execute(text(f"SELECT COUNT(*) FROM {Enregistrement2023DB.__tablename__} "
                                          f"WHERE id_reference IN "
                                          f"(SELECT id_reference_biblio_livre FROM {HelperAuthorBook2023.__tablename__} "
                                          f"WHERE id_author = {id_author} )"))
            for i in res:
                return i[0]

    @staticmethod
    def get_records_by_ref(id_ref, n_page, size, sort_by):
        the_query = Enregistrement2023DB.query
        the_query = the_query.join(Enregistrement2023DB.reference)
        the_query = the_query.filter(ReferenceBibliographiqueLivre2023DB.id == id_ref)
        return [dict(type="record", description=str(rec_db), id=rec_db.id)
                for rec_db in the_query.paginate(page=n_page, per_page=size).items]

    @staticmethod
    def get_records_by_ref_count(id_ref):
        the_query = Enregistrement2023DB.query
        the_query = the_query.join(Enregistrement2023DB.reference)
        the_query = the_query.filter(ReferenceBibliographiqueLivre2023DB.id == id_ref)
        return the_query.count()


class EmpruntLivre:
    @staticmethod
    def from_data_to_db(emprunt: dict) -> EmpruntLivre2023DB:
        emprunt_livre_2023_db = EmpruntLivre2023DB()
        emprunt_livre_2023_db.id_emprunteur = emprunt["id_emprunteur"]
        emprunt_livre_2023_db.id_enregistrement = emprunt["id_enregistrement"]
        emprunt_livre_2023_db.id_gestionnaire = emprunt["id_gestionnaire"]
        emprunt_livre_2023_db.commentaire = emprunt["commentaire"]
        emprunt_livre_2023_db.emprunte = emprunt["emprunte"]
        emprunt_livre_2023_db.date_emprunt = emprunt["date_emprunt"]
        emprunt_livre_2023_db.date_retour_prevu = emprunt["date_retour_prevu"]
        emprunt_livre_2023_db.date_retour_reel = emprunt["date_retour_reel"]
        emprunt_livre_2023_db.rendu = emprunt["rendu"]
        return emprunt_livre_2023_db



    @staticmethod
    def from_db_to_data(emprunt_db: EmpruntLivre2023DB):
        date_retour_reel_string = ""
        date_emprunt_string = ""
        date_retour_prevu_string = ""
        if emprunt_db.date_retour_reel:
            date_retour_reel_string = DateHeureUtils.date_to_vue_str(emprunt_db.date_retour_reel)
        if emprunt_db.date_emprunt:
            date_emprunt_string = DateHeureUtils.date_to_vue_str(emprunt_db.date_emprunt)
        if emprunt_db.date_retour_prevu:
            date_retour_prevu_string = DateHeureUtils.date_to_vue_str(emprunt_db.date_retour_prevu)
        return dict(
            id=emprunt_db.id,
            id_gestionnaire=emprunt_db.id_gestionnaire,
            gestionnaire=User2023.from_db_to_data(emprunt_db.gestionnaire),
            id_enregistrement=emprunt_db.id_enregistrement,
            enregistrement=Enregistrement2023.from_db_to_data(emprunt_db.enregistrement),
            id_emprunteur=emprunt_db.id_emprunteur,
            emprunteur=User2023.from_db_to_data(emprunt_db.emprunteur),
            comment=emprunt_db.commentaire,
            emprunte=emprunt_db.emprunte,
            date_emprunt=date_emprunt_string,
            date_retour_prevu=date_retour_prevu_string,
            date_retour_reel=date_retour_reel_string,
            rendu=emprunt_db.rendu
        )

    @staticmethod
    def is_book_being_borrowed(id_enregistrement: int):
        borrowings_db = EmpruntLivre2023DB.query.filter_by(
            id_enregistrement=id_enregistrement,
            emprunte=True,
            rendu=False).all()
        return len(borrowings_db) > 0

    @staticmethod
    def get_all_book_borrowings(id_enregistrement: int):
        return [EmpruntLivre.from_db_to_data(borrowing_db)
                for borrowing_db in EmpruntLivre2023DB.query.filter_by(id_enregistrement=id_enregistrement).all()]


class User2023:
    @classmethod
    def from_id_to_user_data(cls, _user_id: int) -> Optional[Dict]:
        user_db = UserDB.query.filter_by(id=_user_id).first()
        if user_db:
            return cls.from_db_to_data(user_db)
        return None

    @classmethod
    def from_email_address_to_user(cls, email_address: str):
        user_db = UserDB.query.filter_by(email=email_address).first()
        if user_db:
            return cls.from_db_to_data(user_db)
        return None

    @staticmethod
    def from_db_to_data(user_db: UserDB):
        date_inscription_str = ""
        if user_db.date_inscription:
            date_inscription_str = DateHeureUtils.date_to_vue_str(user_db.date_inscription)
        return dict(
            first_name=user_db.first_name,
            family_name=user_db.family_name,
            email=user_db.email,
            right=user_db.right.value,
            id=user_db.id,
            date_inscription=date_inscription_str
        )

    @staticmethod
    def from_data_to_db(user: dict):
        user_db = UserDB()
        user_db.first_name = user["first_name"]
        user_db.family_name = user["family_name"]
        user_db.email = user["email"]
        user_db.right = user["right"]
        user_db.id = user["id"]
        # user_db.date_inscription = user["date_inscription"]


class LogEvent:
    @staticmethod
    def from_db_to_data(event_db: LogEventDB):
        return dict(
            id=event_db.id,
            event_type=event_db.event_type.value,
            object_id=event_db.object_id,
            event_datetime=DateHeureUtils.datetime_to_str(event_db.event_datetime),
            event_owner_id=event_db.event_owner_id,
            table_name=event_db.table_name,
            values=event_db.values
        )

    @staticmethod
    def from_data_to_db(event: dict):
        log_event_db = LogEventDB()
        log_event_db.id = event.get("id")
        log_event_db.event_type = event.get("event")
        log_event_db.object_id = event.get("object_id")
        log_event_db.event_datetime = datetime.datetime.fromisoformat(event.get("event_datetime"))
        log_event_db.event_owner_id = event.get("event_owner_id")
        log_event_db.table_name = event.get("table_name")
        log_event_db.values = event.get("values")
        return log_event_db


class Import:
    @staticmethod
    def from_db_to_data(import_db: ImportDB):
        return dict(id=import_db.id_,
                    filename=import_db.filename,
                    start_date=import_db.start_date,
                    end_date=import_db.end_date,
                    id_user=import_db.id_user,
                    description=import_db.description,
                    status=import_db.status,
                    selected_method=import_db.selected_method)

    @staticmethod
    def from_data_to_db(import_data: dict):
        import_db = ImportDB()
        import_db.id_ = import_data.get("id", None)
        import_db.filename = import_data.get("filename", None)
        import_db.start_date = import_data.get("start_date", None)
        import_db.end_date = import_data.get("end_date", None)
        import_db.id_user = import_data.get("id_user", None)
        import_db.description = import_data.get("description", None)
        import_db.status = import_data.get("status", None)
        import_db.selected_method = import_data.get("selected_method", None)
        return import_db



    @staticmethod
    def get_all_imports(filter_by_description: str, n_page: int, size: int):
        if filter_by_description:
            imports_db = ImportDB.query\
                .filter_by(description=filter_by_description)\
                .paginate(page=n_page, per_page=size).all()
        else:
            imports_db = ImportDB.query\
                .paginate(page=n_page, per_page=size)\
                .all()
        imports = [Import.from_db_to_data(import_db) for import_db in imports_db]
        return imports

    @staticmethod
    def save_import(import_db: ImportDB):
        db.session.add(import_db)
        db.session.commit()

    @staticmethod
    def delete_import_by_id(import_id: int):
        import_db = ImportDB.query.filter_by(id_=import_id).first()
        if import_db:
            db.session.delete(import_db)
            db.session.commit()

    @staticmethod
    def delete_import(import_db: ImportDB):
        db.session.delete(import_db)
        db.session.commit()

    @staticmethod
    def get_import_by_filename(filename: str):
        import_db = ImportDB.query.filter_by(filename=filename).first()
        if import_db:
            return Import.from_db_to_data(import_db)
        # TODO
        return None

    @staticmethod
    def get_import_db_by_id(id_: int) -> Optional[ImportDB]:
        return ImportDB.query.filter_by(id_=id_).first()

    # @staticmethod
    # def update_import_db_by_id(import_id: int, data):
    #     import_db = ImportDB.query.filter_by(id_=import_id).first()
    #     import_db
    #     db.session.commit()





