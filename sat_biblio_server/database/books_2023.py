"""

"""
import abc
import datetime

from sat_biblio_server.database.db_manager import db
from sat_biblio_server.database.users import UserDB

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

HelperAuthorBook2023 = db.Table('helperauthorbook2023',
                            db.Column("id_author", db.Integer, db.ForeignKey("Author2023.id")),
                            db.Column("id_reference_biblio_livre", db.Integer, db.ForeignKey("ReferenceBibliographiqueLivre2023.id")),
                            extend_existing=True)
HelperAuthorBook2023.__tablename__ = 'helperauthorbook2023'
# HelperAuthorArticle = db.Table('helperauthorarticle',
#                                db.Column("id_author", db.Integer, db.ForeignKey("author.id"), primary_key=True),
#                                db.Column("id_reference_biblio_article", db.Integer,
#                                          db.ForeignKey("reference_biblio_article.id"), primary_key=True)
#                                )

class CsvMeta(abc.ABC):

    @abc.abstractmethod
    def export_to_csv_line(self) -> str:
        pass

    @abc.abstractmethod
    def export_to_prettify_line(self) -> str:
        pass

    @abc.abstractmethod
    def afficher_tooltip(self) -> str:
        """

        :return:
        """
        pass

    @abc.abstractmethod
    def get_csv_fieldnames(self) -> str:
        """

        :return:
        """
        pass


class Author2023DB(db.Model):
    """
    Un auteur est une personne physique qui a écrit un livre ou qui a participé à l'élaboration du contenu d'un
    ouvrage.

    On pourrait rajouter comme informations :
    - commentaire
    - lien vers une page Wikipédia, par exemple
    -

    """
    __tablename__ = "Author2023"
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    family_name = db.Column(db.String(50))
    # region meta
    valide = db.Column(db.Boolean, default=False)
    origin = db.Column(db.String(50), default="")
    date_derniere_modification = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    # endregion
    reference_biblio_livres = db.relationship("ReferenceBibliographiqueLivre2023DB", secondary=HelperAuthorBook2023,
                                              back_populates="authors")

    def __str__(self):
        return f"{self.first_name} {self.family_name}"

    def afficher_tooltip(self):
        return "Prénom : {}\nNom : {}".format(self.first_name, self.family_name)

    def export_to_prettify_line(self):
        return "{} ({})".format(self.family_name, self.first_name)

    def export_to_csv_line(self):
        return self.export_to_prettify_line()

    @staticmethod
    def get_csv_fieldnames():
        return ["Auteur"]


class ReferenceBibliographiqueLivre2023DB(db.Model):
    """
    Un livre est caractérisé par
    - un ou plusieurs auteurs
    - un titre
    - un lieu d'édition
    - éditeur ou par défaut un imprimeur
    - nombre de pages

    On parle vraiment de ce qui est propre à un livre.

    """
    __tablename__ = "ReferenceBibliographiqueLivre2023"
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    authors = db.relationship(Author2023DB, secondary=HelperAuthorBook2023, back_populates="reference_biblio_livres")
    titre = db.Column(db.String(200), nullable=False)
    lieu_edition = db.Column(db.String(100), default="s.l.")
    editeur = db.Column(db.String(50), default="s.n.")
    annee = db.Column(db.String(10))
    nb_page = db.Column(db.String(10))
    # region meta
    origin = db.Column(db.String(50), default="")
    date_derniere_modification = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    # valide = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(500), default="")
    # endregion

    def __str__(self):
        return " ".join([auteur.__str__() for auteur in self.authors]) + \
               " " + self.titre + " " + self.lieu_edition + " " + self.editeur + " " + str(self.annee) + " " + \
               self.nb_page

    def afficher_tooltip(self) -> str:
        """
        Quand on survole une référence bibliographique, on affiche ces informations.
        :return:
        """
        return "{}\nTitre : {}\nLieu d'édition : {}\nEditeur : {}\nAnnée : {}\nNombre de pages : {}".format(
            " ".join([auteur.afficher_tooltip() for auteur in self.authors.all()]), self.titre, self.lieu_edition,
            self.editeur,
            str(self.annee), self.nb_page)

    def export_to_csv_line(self) -> str:
        """
        Exportation du contenu de la base en une forme lisible sous la forme d'une ligne CSV.
        :return: CSV line
        """
        return "\t".join([", ".join([auteur.export_to_csv_line() for auteur in self.authors.all()]), self.titre,
                          self.lieu_edition, self.editeur, str(self.annee), self.nb_page, self.description.__str__()])

    @staticmethod
    def get_csv_fieldnames() -> str:
        """
        Les champs d'une ligne CSV.
        :return:
        """
        return "\t".join([Author2023DB.get_csv_fieldnames(), "Titre", "Editeur (lieu d'édition)",
                          "Année d'édition", "Description"])


# class ReferenceBibliographiqueArticleDB(db.Model):
#     """
#     Un article est une document publié dans une revue paraissant périodiquement.
#     Un article est caractérisé par :
#     - un ou plusieurs auteurs
#     - un titre
#     - le tome dans lequel il est apparu
#     - le numéro de ce tome
#     - le nombre de pages.
#     """
#     __tablename__ = "ReferenceBibliographiqueArticle"
#     __table_args__ = {'sqlite_autoincrement': True}
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # id_author = db.Column(db.Integer, db.ForeignKey('author.id'))
#     authors = db.relationship('Author', secondary=HelperAuthorArticle, backref='ReferenceBibliographiqueArticle')
#     titre = db.Column(db.String(200))
#
#     tome = db.Column(db.String(200))
#     numero = db.Column(db.Integer)
#     nb_page = db.Column(db.String(10))
#
#     def __str__(self):
#         return " ".join([auteur.__str__() for auteur in self.authors.all()]) + " " + self.titre + " " + self.tome + \
#                " " + str(self.numero) + " " + self.nb_page
#
#     def afficher_tooltip(self):
#         """
#
#         :return:
#         """
#         return "{}\nTitre : {}\nTome : {}\nNuméro : {}\nNombre de pages : {}".format(
#             " ".join([auteur.afficher_tooltip() for auteur in self.authors.all()]), self.titre, self.tome, self.numero,
#             self.nb_page)


class Enregistrement2023DB(db.Model):
    """
    Enregistrement tel que décrit dans le fichier principal qui est l'inventaire.
    C'est pour repérer un livre dans la bibliothèque.
    Les renseignements nécessaires sont :
    - description, qui est la référence bibliographique du livre
    - la côte du livre dans la bibliothèque
    - l'année d'obtention du livre
    - le nombre d'exemplaires de livres possédés
    - la provenance du livre (par un don, un achat, etc)
    - un champ texte contenant des mots-clef
    - la date de modification de la fiche
    - est-ce une fiche validée par le gestionnaire de la bibliothèque ?
        Si oui, alors la fiche est consultable par un utilisateur, si non, cela ne pourra pas être lu.
        #TODO Doit-on conserver toutes les versions des fiches ? Je crois que non, on conservera régulièrement
        des copies de la base de données.

    """
    __tablename__ = "Enregistrement2023"
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # description = models.CharField(max_length=1000, verbose_name="description", null=True, default="")
    id_reference = db.Column(db.Integer, db.ForeignKey('ReferenceBibliographiqueLivre2023.id'))
    reference = db.relationship(ReferenceBibliographiqueLivre2023DB)  # , on_delete=models.CASCADE)
    commentaire = db.Column(db.String(500), default="")
    cote = db.Column(db.String(100), nullable=True, default="")
    annee_obtention = db.Column(db.String(20), nullable=True, default="")
    # nb_exemplaire_supp = db.Column(db.String(50), nullable=True, default=0)
    provenance = db.Column(db.String(100), nullable=True, default="")
    aide_a_la_recherche = db.Column(db.String(500), nullable=True, default="")
    observations = db.Column(db.String(10000), default="")
    # region meta
    date_desherbe = db.Column(db.DateTime, default=None, nullable=True)
    colonne_schweitz = db.Column(db.String(200), default="")
    date_derniere_modification = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    valide = db.Column(db.Boolean, default=False)
    origin = db.Column(db.String(50), default="")  # from "import"
    row = db.Column(db.String(500), default="")
    # endregion

    def __str__(self):
        return f"cote={self.cote}, annee={self.annee_obtention} "\
               f"provenance={self.provenance} observations={self.observations} "\
               f"aide_a_la_recherche={self.aide_a_la_recherche}, commentaire={self.commentaire} "\
               f"date_desherbe={self.date_desherbe}, date_derniere_modification={self.date_derniere_modification}"\
               f"valide={self.valide}, origin={self.origin}"

    def afficher_tooltip(self):
        return """Cote : {}\nAnnée : {}\nObservations : {}\nProvenance : {}""".format(
            self.cote, self.annee_obtention, self.observations, self.provenance)

    def export_to_csv_line(self):
        line = [self.cote, self.annee_obtention, self.observations, self.provenance,
                self.aide_a_la_recherche, self.row]
        print(line)
        return "\t".join(line)

    def export_to_prettify_line(self):
        return f"{self.cote}"

    @staticmethod
    def get_csv_fieldnames() -> str:
        return "\t".join(
            [ReferenceBibliographiqueLivre2023DB.get_csv_fieldnames(), "Cote", "Observations", "Provenance", "Entrée bibliothèque",
             "Aide à la recherche"])


class EmpruntLivre2023DB(db.Model):
    """
    L'emprunt d'un livre est fait par un emprunteur.
    Un gestionnaire supervise un emprunt.
    Le livre emprunté est soigneusement noté.
    Il y a une date de retour du livre prévu.
    Et on note quand il revient.
    """
    __tablename__ = "EmpruntLivre2023"
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_emprunteur = db.Column(db.Integer, db.ForeignKey('User.id'))
    emprunteur = db.relationship(UserDB, primaryjoin=id_emprunteur == UserDB.id)  # , related_name="emprunteur", on_delete=models.SET_NULL, null=True)
    id_enregistrement = db.Column(db.Integer, db.ForeignKey('Enregistrement2023.id'))
    enregistrement = db.relationship(Enregistrement2023DB, primaryjoin=id_enregistrement == Enregistrement2023DB.id)  # , on_delete=models.SET_NULL, null=True)
    id_gestionnaire = db.Column(db.Integer, db.ForeignKey('User.id'))
    gestionnaire = db.relationship(UserDB, primaryjoin=id_gestionnaire == UserDB.id)  # , related_name="gestionnaire", on_delete=models.SET_NULL, null=True)

    commentaire = db.Column(db.String())
    emprunte = db.Column(db.Boolean, default=True)
    date_emprunt = db.Column(db.Date, default=datetime.datetime.now())
    date_retour_prevu = db.Column(db.Date)
    date_retour_reel = db.Column(db.Date)
    rendu = db.Column(db.Boolean)

    def __repr__(self):
        date_string = ""
        if self.date_retour_reel:
            date_string = self.date_retour_reel.isoformat()
        if self.date_emprunt:
            date_string += f"|{self.date_emprunt.isoformat()}|"
        if self.date_retour_prevu:
            date_string += f"|{self.date_retour_prevu.isoformat()}|"

        return f"Emprunteur: {self.emprunteur}, enregistrement: {self.enregistrement}, emprunte: {self.emprunte}, " \
               f"dates {date_string}, commentaire: {self.commentaire}, (gestionnaire: {self.gestionnaire})"
