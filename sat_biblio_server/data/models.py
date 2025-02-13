"""

"""

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

import abc
import datetime
import logging
from typing import Union, List, Dict

from sat_biblio_server.database.books import AuthorDB, ReferenceBibliographiqueLivreDB, EnregistrementDB, EmpruntLivreDB, \
    UserDB
from sat_biblio_server.database.events import LogEventDB
from sat_biblio_server.database.imports import ImportDB
from sat_biblio_server.database import db
from sqlalchemy import and_, join

from sat_biblio_server.utils import DateHeureUtils


def date_to_str(date: Union[None, datetime.date]) -> str:
    if date:
        return date.strftime("%d/%m/%Y")
        # return date.isoformat()  # strftime("%d/%m/%Y")
    return ""


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



class Author(IoData):

    def __init__(self, **kwargs):
        self.first_name = kwargs.get("first_name", "")
        self.family_name = kwargs.get("family_name", "")

    def __str__(self):
        return f"{self.first_name} {self.family_name}"

    def __repr__(self):
        return f"<Author> {self}"

    @staticmethod
    def from_db_to_data(author_db: AuthorDB):
        if author_db:
            return dict(
                first_name=author_db.first_name,
                family_name=author_db.family_name,
                id=author_db.id,
                valide=author_db.valide
            )
        else:
            return {}

    @staticmethod
    def from_data_to_db(author):
        author_db = AuthorDB()
        if "first_name" in author:
            author_db.first_name = author["first_name"]
        if "id" in author:
            author_db.id = author["id"]
        if "family_name" in author:
            author_db.family_name = author["family_name"]
        if "valide" in author:
            author_db.valide = author["valide"]
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
        return AuthorDB.query.filter_by(id=id_).first()

    @staticmethod
    def from_ids_to_db(ids):
        return [Author.from_id_to_db(id_) for id_ in ids]

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
        the_query = AuthorDB.query
        the_query = the_query.join(ReferenceBibliographiqueLivreDB.authors)
        the_query = the_query.filter(ReferenceBibliographiqueLivreDB.id == id_ref)
        return [dict(type="author", description=str(author), id=author.id)
                for author in the_query.paginate(page=n_page, per_page=size).items]

    @staticmethod
    def get_authors_by_ref_count(id_ref):
        """
        select * from authors where

        :param id_ref:
        :return:
        """
        the_query = AuthorDB.query
        the_query = the_query.join(ReferenceBibliographiqueLivreDB.authors)
        the_query = the_query.filter(ReferenceBibliographiqueLivreDB.id == id_ref)
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
        refs_db = ReferenceBibliographiqueLivreDB.query.filter(
            and_(EnregistrementDB.reference,
                 EnregistrementDB.id == id_record)).all()
        logging.warning(refs_db)
        refs = [ReferenceBibliographiqueLivre.from_db_to_data(ref) for ref in refs_db]
        logging.warning(refs)
        if refs:
            the_query = AuthorDB.query.filter(
                and_(ReferenceBibliographiqueLivreDB.authors,
                     ReferenceBibliographiqueLivreDB.id == refs[0]["id"]))
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
        refs_db = ReferenceBibliographiqueLivreDB.query.filter(
            and_(EnregistrementDB.reference,
                 EnregistrementDB.id == id_record)).all()
        logging.warning(refs_db)
        refs = [ReferenceBibliographiqueLivre.from_db_to_data(ref) for ref in refs_db]
        logging.warning(refs)
        if refs:
            the_query = AuthorDB.query.filter(
                and_(ReferenceBibliographiqueLivreDB.authors,
                     ReferenceBibliographiqueLivreDB.id == refs[0]["id"]))
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
        the_query = AuthorDB.query.filter(AuthorDB.id.not_in(ReferenceBibliographiqueLivreDB.authors))
        return [dict(type="author", description=str(author), id=author.id)
                for author in the_query.paginate(page=n_page, per_page=size).items]


class ReferenceBibliographiqueLivre(IoData):

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
        if "valide" in reference:
            reference_db.valide = reference["valide"]
        else:
            reference_db.valide = False
        if "description" in reference:
            reference_db.description = reference["description"]

        return reference_db

    @staticmethod
    def from_db_to_data(reference: ReferenceBibliographiqueLivreDB):
        if reference:
            return dict(
                id=reference.id,
                authors=[Author.from_db_to_data(author_db) for author_db in reference.authors],
                titre=reference.titre,
                lieu_edition=reference.lieu_edition,
                editeur=reference.editeur,
                annee=reference.annee,
                nb_page=reference.nb_page,
                valide=reference.valide,
                description=reference.description
            )
        else:
            return {}

    # region CSV & Excel
    @staticmethod
    def from_data_to_csv_row(data: dict) -> List:
        return [
            " ; ".join([Author.from_data_to_csv_row(author_data) for author_data in data.get("authors", [])]),
            data.get("titre", ""),
            data.get("lieu_edition", "s. l."),
            data.get("editeur", "s. e."),
            data.get("annee", "s. a."),
            data.get("nb_page", ""),
            data.get("description", "")
        ]

    @staticmethod
    def get_column_names():
        return Author.get_column_names() + \
            ["Titre", "Lieu d'édition", "Editeur", "Année d'édition",
             "Nombre de pages", "Description"]
    # endregion

    @staticmethod
    def from_id_to_db(id_):
        return ReferenceBibliographiqueLivreDB.query.filter_by(id=id_).first()

    @staticmethod
    def from_ids_to_db(ids):
        return [ReferenceBibliographiqueLivre.from_id_to_db(id_) for id_ in ids]

    @staticmethod
    def get_references_by_author(id_author, n_page, size, sort_by):
        """
        >>> ReferenceBibliographiqueLivre.get_references_by_author(12, 0, 0, 0)

        :param id_author:
        :param n_page:
        :param size:
        :param sort_by:
        :return:
        """

        res = db.engine.execute(f"SELECT * FROM {ReferenceBibliographiqueLivreDB.__tablename__} "
                                f"WHERE id IN "
                                f"(SELECT id_reference_biblio_livre FROM helperauthorbook "
                                f"WHERE id_author = {id_author}) LIMIT {size} OFFSET {(n_page - 1) * size}")
        # print([i.values() for i in res])
        # return res.first().values()[0]
        return [dict(type="reference", description=str(ref_db["titre"])+" "+ref_db["editeur"], id=ref_db["id"])
                for ref_db in res.fetchall()]

        # the_query = ReferenceBibliographiqueLivreDB.query
        # the_query = the_query.filter(ReferenceBibliographiqueLivreDB.authors.any(id=id_author))
        # the_query = ReferenceBibliographiqueLivreDB.authors.any(id=id_author)
        # return [dict(type="reference", description=str(ref_db), id=ref_db.id)
        #         for ref_db in the_query.paginate(page=n_page, per_page=size).items]

    @staticmethod
    def get_references_by_author_count(id_author):
        """
        >>> ReferenceBibliographiqueLivre.get_references_by_author(12, 0, 0, 0)

        :param id_author:
        :return:
        """
        res = db.engine.execute(f"SELECT COUNT(*) FROM {ReferenceBibliographiqueLivreDB.__tablename__} "
                                f"WHERE id IN "
                                f"(SELECT id_reference_biblio_livre FROM helperauthorbook "
                                f"WHERE id_author = {id_author} )")
        # print([i.values() for i in res])
        return res.first().values()[0]
        # the_query = ReferenceBibliographiqueLivreDB.query
        # the_query = the_query.filter(ReferenceBibliographiqueLivreDB.authors.any(id=id_author))
        # return the_query.count()

    @staticmethod
    def get_references_by_record(id_record, n_page, size, sort_by):
        """

        :param id_record:
        :param n_page:
        :param size:
        :param sort_by:
        :return:
        """
        the_query = ReferenceBibliographiqueLivreDB.query
        the_query = the_query.join(EnregistrementDB.reference)
        the_query = the_query.filter(EnregistrementDB.id == id_record)
        return [dict(type="reference", description=str(ref_db), id=ref_db.id)
                for ref_db in the_query.paginate(page=n_page, per_page=size).items]

    @staticmethod
    def get_references_by_record_count(id_record):
        """

        :param id_record:
        :return:
        """
        the_query = ReferenceBibliographiqueLivreDB.query
        the_query = the_query.join(EnregistrementDB.reference)
        the_query = the_query.filter(EnregistrementDB.id == id_record)
        return the_query.count()


class Enregistrement(IoData):

    def __init__(self):
        self.cote = ""

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
        if "commentaire" in enregistrement:
            enregistrement_db.commentaire = enregistrement["commentaire"]
        if "row" in enregistrement:
            enregistrement_db.row = enregistrement["row"]
        return enregistrement_db

    @staticmethod
    def from_db_to_data(enregistrement_db: EnregistrementDB) -> dict:
        if enregistrement_db:
            return dict(
                id=enregistrement_db.id,
                reference=ReferenceBibliographiqueLivre.from_db_to_data(enregistrement_db.reference),
                annee=enregistrement_db.annee,  # année d'obtention
                commentaire=enregistrement_db.commentaire,
                cote=enregistrement_db.cote,
                nb_exemplaire_supp=enregistrement_db.nb_exemplaire_supp,
                provenance=enregistrement_db.provenance,
                mots_clef=enregistrement_db.mots_clef,
                date_modification=enregistrement_db.date_modification,
                valide=enregistrement_db.valide,
                row=enregistrement_db.row)
        else:
            return {}

    # region CSV & Excel
    @staticmethod
    def from_data_to_csv_row(data: dict):
        return ReferenceBibliographiqueLivre.from_data_to_csv_row(data.get("reference")) + \
            [
                data.get("annee", ""),
                data.get("commentaire", ""),
                data.get("cote", ""),
                data.get("nb_exemplaire_supp", ""),
                data.get("provenance", ""),
                data.get("mots_clef", ""),
                # data.get("date_modification", ""),
                data.get("row", "")
               ]

    @staticmethod
    def get_column_names():
        return ReferenceBibliographiqueLivre.get_column_names() + \
            ["Année", "Commentaire", "Cote", "Nombre d'exemplaire supplémentaire",
             "Provenance", "Mots-clefs", "Ligne"]
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
        request = f"SELECT * FROM {EnregistrementDB.__tablename__} " \
                  f"WHERE id_reference IN " \
                  f"(SELECT id_reference_biblio_livre FROM helperauthorbook " \
                  f"WHERE id_author = {id_author}) LIMIT {size} OFFSET {(n_page-1)*size} "
        res = db.engine.execute(request)
        return [dict(type="record", description=str(rec_db.__str__()), id=rec_db["id"])
                for rec_db in res.fetchall()]

        # the_query = EnregistrementDB.query
        # the_query = the_query.join(EnregistrementDB.reference)
        # the_query = the_query.filter(ReferenceBibliographiqueLivreDB.authors.any(id=id_author))
        # return [dict(type="record", description=str(rec_db), id=rec_db.id)
        #         for rec_db in the_query.paginate(page=n_page, per_page=size).items]

    @staticmethod
    def get_records_by_author_count(id_author):
        """

        :param id_author:
        :return:
        """
        res = db.engine.execute(f"SELECT COUNT(*) FROM {EnregistrementDB.__tablename__} "
                          f"WHERE id_reference IN "
                          f"(SELECT id_reference_biblio_livre FROM helperauthorbook "
                          f"WHERE id_author = {id_author} )")
        # print(help(res))
        # b = RowProxy()

        return res.first().values()[0]
        # the_query = EnregistrementDB.query
        # the_query = the_query.join(EnregistrementDB.reference)
        # the_query = EnregistrementDB.reference
        # the_query = the_query.filter(ReferenceBibliographiqueLivreDB.authors.any(id=id_author))
        # return the_query.count()

    @staticmethod
    def get_records_by_ref(id_ref, n_page, size, sort_by):
        the_query = EnregistrementDB.query
        the_query = the_query.join(EnregistrementDB.reference)
        the_query = the_query.filter(ReferenceBibliographiqueLivreDB.id == id_ref)
        return [dict(type="record", description=str(rec_db), id=rec_db.id)
                for rec_db in the_query.paginate(page=n_page, per_page=size).items]

    @staticmethod
    def get_records_by_ref_count(id_ref):
        the_query = EnregistrementDB.query
        the_query = the_query.join(EnregistrementDB.reference)
        the_query = the_query.filter(ReferenceBibliographiqueLivreDB.id == id_ref)
        return the_query.count()


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
            gestionnaire=User.from_db_to_data(emprunt_db.gestionnaire),
            id_enregistrement=emprunt_db.id_enregistrement,
            enregistrement=Enregistrement.from_db_to_data(emprunt_db.enregistrement),
            id_emprunteur=emprunt_db.id_emprunteur,
            emprunteur=User.from_db_to_data(emprunt_db.emprunteur),
            comment=emprunt_db.commentaire,
            emprunte=emprunt_db.emprunte,
            date_emprunt=date_emprunt_string,
            date_retour_prevu=date_retour_prevu_string,
            date_retour_reel=date_retour_reel_string,
            rendu=emprunt_db.rendu
        )

    @staticmethod
    def is_book_being_borrowed(id_enregistrement: int):
        borrowings_db = EmpruntLivreDB.query.filter_by(
            id_enregistrement=id_enregistrement,
            emprunte=True,
            rendu=False).all()
        return len(borrowings_db) > 0

    @staticmethod
    def get_all_book_borrowings(id_enregistrement: int):
        return [EmpruntLivre.from_db_to_data(borrowing_db)
                for borrowing_db in EmpruntLivreDB.query.filter_by(id_enregistrement=id_enregistrement).all()]


class User:
    @staticmethod
    def from_db_to_data(user_db: UserDB):
        return dict(
            first_name=user_db.first_name,
            family_name=user_db.family_name,
            email=user_db.email,
            right=user_db.right.value,
            id=user_db.id,
            confirmed=user_db.confirmed
        )

    @staticmethod
    def from_data_to_db(user: dict):
        return UserDB(first_name=user["first_name"],
                      family_name=user["family_name"],
                      email=user["email"],
                      right=user["right"],
                      id=user["id"])


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
        return LogEventDB(id=event.get("id"),
                          event_type=event.get("event"),
                          object_id=event.get("object_id"),
                          event_datetime=datetime.datetime.fromisoformat(event.get("event_datetime")),
                          event_owner_id=event.get("event_owner_id"),
                          table_name=event.get("table_name"),
                          values=event.get("values"))


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
        return ImportDB(id=import_data.get("id"),
                        filename=import_data.get("filename"),
                        start_date=import_data.get("start_date"),
                        end_date=import_data.get("end_date"),
                        id_user=import_data.get("id_user"),
                        description=import_data.get("description"),
                        status=import_data.get("status"),
                        selected_method=import_data.get("selected_method"),
                        )
    @staticmethod
    def get_all_imports():
        imports_db = ImportDB.query.all()
        imports = [Import.from_db_to_data(import_db) for import_db in imports_db]
        return imports

    @staticmethod
    def save_import(import_db: ImportDB):
        db.session.add(import_db)
        db.session.commit()



