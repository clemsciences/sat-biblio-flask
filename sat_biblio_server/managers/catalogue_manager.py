"""

"""
import datetime
from collections import defaultdict
import re
from typing import List, Optional, Dict, Union

from sat_biblio_server import ReferenceBibliographiqueLivre2023DB, Enregistrement2023DB
from sat_biblio_server.data.models_2023 import Author2023, \
    ReferenceBibliographiqueLivre2023, Enregistrement2023


# region catalogue schweitz
class CatalogueSchweitz:
    COLUMNS = ["Auteurs - Titres - Editeurs - Année", "cote", "Nb ex sup", "année entrée", "Provenance",
               "lieu-personnage", "mot clé 1", "mot clé 2",
               "Observations pour transfert sur l'inventaire forme 2022"]

    def __init__(self):
        self.rows: List[CatalogueSchweitzRow] = []

    def parse_rows(self, rows):
        for row in rows:
            schweitz_row = CatalogueSchweitzRow()
            schweitz_row.parse_row(row)
            self.rows.append(schweitz_row)


class CatalogueSchweitzRow:

    def __init__(self):
        self.auteurs_titres_editeurs_annee = ""
        self.cote = ""
        self.nb_ex_sup = 0
        self.annee_entree = ""
        self.provenance = ""
        self.lieu_personnage = ""
        self.mot_clef_1 = ""
        self.mot_clef_2 = ""
        self.observation_transfert_bht = ""

    def parse_row(self, row: List[str]):
        self.auteurs_titres_editeurs_annee = row[0]
        self.cote = row[1]
        self.nb_ex_sup = row[2]
        self.annee_entree = row[3]
        self.provenance = row[4]
        self.lieu_personnage = row[5]
        self.mot_clef_1 = row[6]
        self.mot_clef_2 = row[7]
        self.observation_transfert_bht = row[8]

    def extract_from_auteurs_titres_editeurs_annee(self):
        description = self.auteurs_titres_editeurs_annee.split(",")
        # print(description)
        # description_auteur = description.split(",")
        limite_auteur = 0
        auteurs = []
        while limite_auteur < len(description):
            field = description[limite_auteur]
            # print("field", repr(field))
            m = re.match(r"(?P<nom>[\w\- '.]+) \((?P<prenom>[ \-'\w.]+)\)", field)
            # print(m)
            if m is not None:
                prenom = m.group("prenom")
                nom = m.group("nom")
            elif "[collectif]" in field.lower():
                prenom = "-"
                nom = "[collectif]"
            elif "[coll.]" in field.lower():
                prenom = "-"
                nom = "[collectif]"
            elif "[anonyme]" in field.lower():
                prenom = "-"
                nom = "[collectif]"
            else:
                break
            limite_auteur += 1
            auteurs.append(dict(first_name=prenom.strip(), family_name=nom.strip().capitalize(), valide=True))
        i = 0
        reste = description[limite_auteur:]
        if len(reste) > 0:
            # is first element a year or a title?
            m_year = re.match(r"^(?P<annee>[0-9 \-]+)$", reste[i])
            if m_year and len(reste) > 1:
                # print("year first")
                annee = m_year.group("annee")
                i += 1
                # region title
                m = re.match(r"\"(?P<titre>[0-9\w '\-.?!]+)\"", reste[i])
                if m:
                    titre = m.group("titre").strip()
                    # print("titre: ", titre)
                else:
                    if len(reste) >= i + 1:
                        titre = reste[i].strip()
                        # print("titre not matched", titre)
                    else:
                        titre = ""
                i += 1
                # endregion

                # region lieu d'édition
                if len(reste) >= i + 1:
                    if reste[i] == "":
                        lieu_edition = "s.l."
                    else:
                        lieu_edition = reste[i]
                else:
                    lieu_edition = ""
                i += 1
                # endregion

                # region éditeur
                if len(reste) >= i + 1:
                    if reste[i] == "":
                        editeur = "s.n."
                    else:
                        editeur = reste[i]
                else:
                    editeur = ""
                # endregion

                # region nombre de pages
                if len(reste) >= i + 1:
                    if reste[i] == "":
                        nb_page = "x.p."
                    else:
                        nb_page = reste[i]
                else:
                    nb_page = ""
                # endregion
            else:
                # region titre
                # print(i, reste[i])
                m = re.match(r"\"(?P<titre>[0-9\w '\-.!?]+)\"", reste[i])
                if m:
                    titre = m.group("titre").strip()
                    # print("titre: ", titre)
                else:
                    if len(reste) >= i + 1:
                        titre = reste[i].strip()
                        # print("titre not matched", titre)
                    else:
                        titre = ""
                i += 1
                # endregion

                # region lieu d'édition
                if len(reste) >= i + 1:
                    if reste[i] == "":
                        lieu_edition = "s.l."
                    else:
                        lieu_edition = reste[i]
                else:
                    lieu_edition = ""
                i += 1
                # endregion

                # region éditeur
                if len(reste) >= i + 1:
                    if reste[i] == "":
                        editeur = "s.n."
                    else:
                        editeur = reste[i]
                else:
                    editeur = ""
                i += 1
                # endregion

                # region année
                if len(reste) >= i + 1:
                    if reste[i] == "":
                        annee = "s.d."
                    else:
                        annee = reste[i]
                else:
                    annee = ""
                i += 1
                # endregion

                # region nombre de pages
                if len(reste) >= i + 1:
                    if reste[i] == "":
                        nb_page = "x.p."
                    else:
                        nb_page = reste[i]
                else:
                    nb_page = ""
                i += 1
                # endregion
            return titre, ", ".join([f"{auteur['family_name']} ({auteur['first_name']})" for auteur in auteurs if auteur]), annee, editeur, nb_page, description
        return "", "", "", "", 0, ""

    def to_csv_row(self):
        return [
            self.auteurs_titres_editeurs_annee,
            self.cote,
            self.nb_ex_sup,
            self.annee_entree,
            self.provenance,
            self.lieu_personnage,
            self.mot_clef_1,
            self.mot_clef_2,
            self.observation_transfert_bht
        ]
# endregion


def normalize_cote(cote: str):
    """
    >>> normalize_cote()
    :param cote:
    :return:
    """
    l = f"{cote}".strip().upper().split(" ")

    i_res = 0
    for i, item in enumerate(l):
        if re.match(r"[0-9./]+", item):
            i_res = i
            break
    if i_res > 0:
        first = " ".join(l[:i_res])
        second = l[i_res]
        rest = l[i_res+1:]
        normalized_second = ""
        point_index = second.find(".")
        slash_index = second.find("/")
        index = -1
        if point_index == -1 and slash_index == -1:
            index = len(second)
        elif point_index != -1:
            index = point_index
        elif slash_index != -1:
            index = slash_index

        if len(second[:index]) >= 1:
            if len(second[:index]) >= 4:
                normalized_second = second
            elif len(second[:index]) == 3:
                normalized_second = f"0{second}"
            elif len(second[:index]) == 2:
                normalized_second = f"00{second}"
            elif len(second[:index]) == 1:
                normalized_second = f"000{second}"
        if rest:
            return f"{first} {normalized_second} {' '.join(rest)}".replace("  ", " ")
        else:
            return f"{first} {normalized_second}".replace("  ", " ")
    else:
        return f"{cote}".strip().upper().replace("  ", " ")


def void_if_none(a):
    if a:
        return a
    return ""


def clean_string(a: str):
    if type(a) == str:
        return a.strip()
    return ""


def clean_integer_as_string(a):
    if type(a) == str:
        return a.replace("'", "").replace("", "").strip()
    return str(a)


# region catalogue hamelain 1
class CatalogueHamelain1:
    COLUMNS = ["Cote SAT de l'ouvrage", "Titre de l'ouvrage", "Auteur", "Année de publication", "Editeur",
               "Nombre de pages", "Entrée dans la bibliothèque", "Observations",
               "Aide à la recherche"]

    def __init__(self):
        self.rows: List[CatalogueHamelain1Row] = []
        self.d = defaultdict(list)

    def parse_rows(self, rows, ignore_n_first_rows=0):
        for i, row in enumerate(rows):
            if i >= ignore_n_first_rows:
                hamelain_1_row = CatalogueHamelain1Row()
                hamelain_1_row.parse_row(row)
                self.rows.append(hamelain_1_row)
        for i, row in enumerate(self.rows):
            self.d[row.cote].append(i)

    def keys(self):
        return self.d.keys()


class CatalogueHamelain1Row:

    def __init__(self):
        self.cote = ""
        self.titre = ""
        self.auteurs = ""
        self.annee_publication = ""
        self.editeur = ""
        self.nb_pages = ""
        self.entree_bibliotheque = ""
        self.observations = ""
        self.aide_a_la_recherche = ""

    def parse_row(self, row):
        self.cote = normalize_cote(row[0])
        self.titre = void_if_none(row[1])
        self.auteurs = void_if_none(row[2])
        self.annee_publication = void_if_none(row[3])
        self.editeur = void_if_none(row[4])
        self.nb_pages = void_if_none(row[5])
        self.entree_bibliotheque = void_if_none(row[6])
        self.observations = void_if_none(row[7])
        self.aide_a_la_recherche = void_if_none(row[8])

    def to_csv_row(self):
        return [
            self.cote,
            self.titre,
            self.auteurs,
            self.annee_publication,
            self.editeur,
            self.nb_pages,
            self.entree_bibliotheque,
            self.observations,
            self.aide_a_la_recherche
        ]
# endregion


# region catalogue hamelain 2
class CatalogueHamelain2:
    COLUMNS = ["Cote", "Titre", "Auteur", "Lieu d'édition", "Editeur",
               "Année d'édition", "Nombre de pages", "Description",
               "Nombre d'exemplaire supplémentaire", "Provenance",
               "Mots-clefs", "Contenu colonne Schweitz", "Ouvrages supprimés (désherbage 2022)"]

    def __init__(self):
        self.rows: List[CatalogueHamelain2Row] = []
        self.d = defaultdict(list)

    def parse_rows(self, rows, ignore_n_first_rows=2):
        for i, row in enumerate(rows):
            if i >= ignore_n_first_rows:
                hamelain_2_row = CatalogueHamelain2Row()
                hamelain_2_row.parse_row(row)
                self.rows.append(hamelain_2_row)
        for i, row in enumerate(self.rows):
            self.d[row.cote].append(i)

    def keys(self):
        return self.d.keys()


class CatalogueHamelain2Row:
    def __init__(self):
        self.cote = ""
        self.auteurs = ""
        self.titre = ""
        self.lieu_edition = ""
        self.editeur = ""
        self.annee_publication = ""
        self.nb_pages = ""
        self.description = ""
        self.nb_exemplaire_suppl = ""
        self.entree_bibliotheque = ""
        self.provenance = ""
        self.mots_clefs = ""
        self.contenu_schweitz = ""
        self.ouvrages_desherbes_2022 = ""

    def parse_row(self, row):
        self.cote = normalize_cote(row[0])
        self.auteurs = void_if_none(row[1])
        self.titre = void_if_none(row[2])
        self.lieu_edition = void_if_none(row[3])
        self.editeur = void_if_none(row[4])
        self.annee_publication = void_if_none(row[5])
        self.nb_pages = void_if_none(row[6])
        self.description = void_if_none(row[7])
        self.nb_exemplaire_suppl = void_if_none(row[8])
        self.provenance = void_if_none(row[9])
        self.mots_clefs = void_if_none(row[10])
        self.contenu_schweitz = void_if_none(row[11])
        self.ouvrages_desherbes_2022 = void_if_none(row[12])

    def to_csv_row(self):
        return [
            self.cote,
            self.auteurs,
            self.titre,
            self.lieu_edition,
            self.editeur,
            self.annee_publication,
            self.nb_pages,
            self.description,
            self.nb_exemplaire_suppl,
            self.provenance,
            self.mots_clefs,
            self.contenu_schweitz,
            self.ouvrages_desherbes_2022
        ]
# endregion


# region catalogue hamelain 3
class CatalogueHamelain3:
    COLUMNS = ["Cote", "Titre", "Auteur", "Année d'édition", "Editeur (lieu d'édition)",
               "Provenance", "Description", "Entrée bibliothèque",
               "Aide à la recherche", "Observations", "Contenu colonne Schweitz",
               "Ouvrages supprimés en 2022", "Vérification effectuée en 2022"]
    COLUMNS_WIDTHS = [12.55, 22, 19.36, 8, 25.55, 17.55, 29.36, 11, 16.55, 13, 62.73, 8.82, 10.36]

    def __init__(self):
        self.rows: List[CatalogueHamelain3Row] = []
        self.d = defaultdict(list)

    @classmethod
    def check_column_names(cls, rows) -> Optional[List]:
        l = []
        if rows:
            for i in range(len(rows[0])):
                if cls.COLUMNS[i] != rows[0][i]:
                    l.append((rows[0][i], cls.COLUMNS[i]))
            return l
        return None


    def parse_rows(self, rows, ignore_n_first_rows=2):
        for i, row in enumerate(rows):
            if i > ignore_n_first_rows:
                hamelain_3_row = CatalogueHamelain3Row()
                hamelain_3_row.parse_row(row)

                self.rows.append(hamelain_3_row)
        self.update_d()

    def update_d(self):
        for i, row in enumerate(self.rows):
            self.d[row.cote].append(i)

    def keys(self):
        return self.d.keys()

    def sort_by_cote(self):
        cotes = sorted(list(set(self.keys())))
        new_rows = []
        for cote in cotes:
            for i_line in self.d[cote]:
                new_rows.append(self.rows[i_line])

        self.rows = new_rows


class CatalogueHamelain3Row:
    def __init__(self):
        self.cote = ""
        self.titre = ""
        self.auteurs = ""
        self.annee_edition = ""
        self.editeur_lieu_edition = ""
        self.provenance = ""
        self.entree_bibliotheque = ""
        self.description = ""
        self.aide_a_la_recherche = ""
        self.observations = ""
        self.contenu_schweitz = ""
        self.ouvrages_desherbes = ""

    def parse_row(self, row):
        self.cote = normalize_cote(row[0])
        self.titre = void_if_none(row[1])
        self.auteurs = void_if_none(row[2])
        self.annee_edition = void_if_none(row[3])
        self.editeur_lieu_edition = void_if_none(row[4])
        self.provenance = void_if_none(row[5])
        self.description = void_if_none(row[6])
        self.entree_bibliotheque = void_if_none(row[7])
        self.aide_a_la_recherche = void_if_none(row[8])
        self.observations = void_if_none(row[9])
        self.contenu_schweitz = void_if_none(row[10])
        self.ouvrages_desherbes = void_if_none(row[11])

    def to_csv_row(self):
        return [
            self.cote,
            self.titre,
            self.auteurs,
            self.annee_edition,
            self.editeur_lieu_edition,
            self.provenance,
            self.description,
            self.entree_bibliotheque,
            self.aide_a_la_recherche,
            self.observations,
            self.contenu_schweitz,
            self.ouvrages_desherbes
        ]
# endregion


# region catalogue 2023
class Catalogue2023:
    COLUMNS = ["Cote", "Titre", "Auteur", "Année d'édition", "Editeur (lieu d'édition)",
               "Observations", "Ouvrages supprimés en 2022", "Provenance et date d'entrée",
               "Description", "Entrée bibliothèque", "Aide à la recherche",
               "Contenu colonne Schweitz", "Vérification effectuée en 2022"]
    COLUMNS_WIDTHS = [12.55, 22, 19.36, 8, 25.55, 17.55, 29.36, 11, 16.55, 13, 62.73, 8.82, 10.36]

    def __init__(self):
        self.rows: List[Catalogue2023Row] = []
        self.column_names = []
        self.d = defaultdict(list)

    def check_column_names(self) -> Optional[List]:
        """

        :return:
        """
        match_ids = []
        # print(f"self.column_names={self.column_names}")
        for column_name in self.COLUMNS:
            if column_name in self.column_names:
                match_ids.append(self.column_names.index(column_name))
            else:
                print(f"{column_name} was not found in import file")
                return [f"{column_name} missing"]
        return match_ids

    def parse_rows(self, rows, ignore_n_first_rows=2):

        # print(f"parse rows: {rows[:2]}")
        for i, row in enumerate(rows):
            if i == ignore_n_first_rows:
                self.column_names = row
            elif i > ignore_n_first_rows:
                row_2023 = Catalogue2023Row()
                row_2023.parse_row(row)
                self.rows.append(row_2023)
        self.update_d()

    def check_rows(self) -> List:
        checks = []
        for row_2023 in self.rows:
            row_2023.check_row()
            checks.append(row_2023)
        return checks

    # def check_rows(self, rows, ignore_n_first_rows=2) -> List:
    #     checks = []
    #     for i, row in enumerate(rows):
    #         if i > ignore_n_first_rows:
    #             row_2023 = Catalogue2023Row()
    #             row_2023.parse_row(row)
    #             row_2023.check_row()
    #             checks.append(row_2023)
    #     return checks

    def update_d(self):
        for i, row in enumerate(self.rows):
            self.d[row.cote].append(i)

    def keys(self):
        return self.d.keys()

    def sort_by_cote(self):
        cotes = sorted(list(set(self.keys())))
        new_rows = []
        for cote in cotes:
            for i_line in self.d[cote]:
                new_rows.append(self.rows[i_line])

        self.rows = new_rows

    def export_to_data(self):
        data = []
        for i, row in enumerate(self.rows):
            data.append(row.extract_book_record())
        return data

    @property
    def rows_filtered_by_verified_entry(self):
        rows = []
        for row in self.rows:
            if row.verified_and_present:
                rows.append(row)
        return rows

    def __repr__(self):
        return f"<Catalogue2023> {len(self.rows)} rows"



class Catalogue2023Row:
    COTE_INDEX = 0
    TITLE_INDEX = 1
    AUTHORS_INDEX = 2
    ANNEE_EDITION_INDEX = 3
    EDITEUR_LIEU_EDITION_INDEX = 4
    OBSERVATIONS_INDEX = 5
    OUVRAGES_SUPPRIMES_INDEX = 6
    PROVENANCE_DATE_ENTREE_INDEX = 7
    HELP_DESCRIPTION_INDEX = 8
    ENTREE_BIBLIOTHEQUE_INDEX = 9
    AIDE_A_LA_RECHERCHE_INDEX = 10
    HELP_CONTENU_SCHWEIZ_INDEX = 11
    VERIFICATION_2022_INDEX = 12

    def __init__(self):
        self.cote = ""
        self.titre = ""
        self.auteurs = ""
        self.annee_edition = ""
        self.editeur_lieu_edition = ""
        self.provenance_date_entree = ""
        self.entree_bibliotheque = ""
        self.help_description = ""
        self.aide_a_la_recherche = ""
        self.observations = ""
        self.help_contenu_schweitz = ""
        self.ouvrages_supprimes_2022 = ""
        self.verification_effectuee_en_2022 = ""

        self.row = None

        self._extracted_authors = None
        self._extracted_book_reference = None
        self._extracted_book_record = None

    def parse_row(self, row):
        if len(row) <= self.VERIFICATION_2022_INDEX:
            raise ValueError("The row is too short. Probably a wrong row.")
        self.cote = normalize_cote(row[self.COTE_INDEX])
        self.titre = void_if_none(row[self.TITLE_INDEX])
        self.auteurs = void_if_none(row[self.AUTHORS_INDEX])
        self.annee_edition = clean_integer_as_string(void_if_none(row[self.ANNEE_EDITION_INDEX]))
        self.editeur_lieu_edition = void_if_none(row[self.EDITEUR_LIEU_EDITION_INDEX])
        self.observations = void_if_none(row[self.OBSERVATIONS_INDEX])
        self.ouvrages_supprimes_2022 = void_if_none(row[self.OUVRAGES_SUPPRIMES_INDEX])
        self.provenance_date_entree = void_if_none(row[self.PROVENANCE_DATE_ENTREE_INDEX])
        self.help_description = void_if_none(row[self.HELP_DESCRIPTION_INDEX])
        self.entree_bibliotheque = void_if_none(row[self.ENTREE_BIBLIOTHEQUE_INDEX])
        self.aide_a_la_recherche = void_if_none(row[self.AIDE_A_LA_RECHERCHE_INDEX])
        self.help_contenu_schweitz = void_if_none(row[self.HELP_CONTENU_SCHWEIZ_INDEX])
        self.verification_effectuee_en_2022 = void_if_none(row[self.VERIFICATION_2022_INDEX])
        self.row = str(row)

    def check_row(self) -> List[bool]:
        return [
            self.check_cote(),
            self.check_title(),
            self.check_auteurs(),
            self.check_edition_year(),
            self.check_editor_and_edition_place(),
            self.check_observations(),
            self.check_deleted_works(),
            self.check_provenance(),
            self.check_help_description(),
            self.check_library_entry(),
            self.check_help_to_research(),
            self.check_help_schweiz(),
            self.check_2022_checks()

        ]
    def check_cote(self) -> bool:
        cote_expression = re.compile(r"^(A|B|C|D|MM|DOC|BBH) [0-9]{1,4}(-([0-9\-]{1,2}|[A-Z]))?$")
        return cote_expression.match(self.cote) is not None

    def check_title(self) -> bool:
        return 0 < len(self.titre) < 500

    def check_auteurs(self) -> bool:
        ok = True
        if self.auteurs == "s. n.":
            return True
        for auteur in self.auteurs.split(","):
            ok = ok and self.check_auteur(auteur)
        return ok

    def check_auteur(self, auteur: str) -> bool:
        return re.match(r"^([\w\- ’.]+ \([ \-’\w.]+\)|\[collectif] \(-\)|\[anonyme] \(-\)|s\. n\.)$", auteur) is not None

    def check_edition_year(self) -> bool:
        if self.annee_edition == "s. d.":
            return True
        if type(self.annee_edition) == str:
            edition_year_expression = re.compile("^((vers )?[0-9]{4}|s\. d\.|[0-9]{4}-[0-9]{4})$")
            # print(f"self.annee_edition->{self.annee_edition}-{type(self.annee_edition)}")
            return edition_year_expression.match(self.annee_edition) is not None
        return type(self.annee_edition) == int

    def check_editor_and_edition_place(self) -> bool:
        if self.editeur_lieu_edition == "s. e. (s. l.)":
            return True
        edition_expression = re.compile(r"(s\. e\.|[\w\- /.’]* \((s\. l\.|[\w\-, /.’]*)\))")
        return edition_expression.match(self.editeur_lieu_edition) is not None

    def check_observations(self) -> bool:
        return True

    def check_deleted_works(self) -> bool:
        return True

    def check_provenance(self) -> bool:
        return True

    def check_help_description(self) -> bool:
        return True

    def check_library_entry(self) -> bool:
        return True

    def check_help_to_research(self) -> bool:
        return True

    def check_help_schweiz(self) -> bool:
        return True

    def check_2022_checks(self) -> bool:
        # print(self.verification_effectuee_en_2022)
        # print(self.verification_effectuee_en_2022.strip().lower() in ["oui", "non", "OUI", "NON"])
        return self.verification_effectuee_en_2022.strip().lower() in ["oui", "non", "OUI", "NON"]

    def to_raw_row(self) -> List[str]:
        return [
            self.cote,
            self.titre,
            self.auteurs,
            self.annee_edition,
            self.editeur_lieu_edition,
            self.observations,
            self.ouvrages_supprimes_2022,
            self.provenance_date_entree,
            self.help_description,
            self.entree_bibliotheque,
            self.aide_a_la_recherche,
            self.help_contenu_schweitz,
            self.verification_effectuee_en_2022
        ]

    def to_csv_row(self) -> List[str]:
        return [
            self.cote,
            self.titre,
            self.auteurs,
            self.annee_edition,
            self.editeur_lieu_edition,
            self.observations,
            self.ouvrages_supprimes_2022,
            self.provenance_date_entree,
            # self.description,
            self.entree_bibliotheque,
            self.aide_a_la_recherche,
            # self.contenu_schweitz,
            self.verification_effectuee_en_2022
        ]

    def extract_authors(self) -> List[Author2023]:
        authors = []
        for auteur in self.auteurs.split(","):
            m = re.match(r"(?P<nom>[\w\- '.]+) \((?P<prenom>[ \-'\w.]+)\)", auteur)
            if m is not None:
                prenom = clean_string(m.group("prenom"))
                nom = clean_string(m.group("nom"))
                author = Author2023(first_name=prenom, family_name=nom)
            else:
                author = Author2023(family_name=clean_string(auteur))
            authors.append(author)
        return authors

    def _extract_publisher_and_publication_place(self):
        m = re.match(r"(?P<editeur>[\w\- '.]+) \((?P<lieu_edition>[ \-'\w.]+)\)", self.editeur_lieu_edition)
        publication_place = ""
        if m is not None:
            publisher = clean_string(m.group("editeur"))
            publication_place = clean_string(m.group("lieu_edition"))
        else:
            publisher = clean_string(self.editeur_lieu_edition)
        return publisher, publication_place

    def _extract_provenance_date_entree(self):
        """

        :return:
        """
        parts = self.provenance_date_entree.split(";")
        if len(parts) == 1:
            return clean_string(parts[0]), ""
        return [clean_string(i) for i in parts[:2]]

    @property
    def authors(self):
        if self._extracted_authors is None:
            self._extracted_authors = self.extract_authors()
        return self._extracted_authors

    @property
    def book_reference(self):
        if self._extracted_book_reference is None:
            self._extracted_book_reference = self.extract_book_reference()
        return self._extracted_book_reference

    @property
    def book_record(self):
        if self._extracted_book_record is None:
            self._extracted_book_record = self.extract_book_record()
        return self._extracted_book_record

    @property
    def page_number(self) -> int:
        """
        TODO complete with more cases
        -1 is the default number of pages (when not found)
        :return:
        """
        if type(self.observations) == str:
            for observation in self.observations.split(";"):
                m = re.match(r"(?P<page_number>[0-9]+) p\.", clean_string(observation))
                if m is not None:
                    return m.group("page_number")
            return -1
        else:
            # C 3563, to add again
            # Provenance et date d’entrée
            # Provenance et date d'entrée
            print(f"self.observations: {self.observations}")

    @property
    def provenance(self):
        return clean_string(self._extract_provenance_date_entree()[0])

    @property
    def annee_obtention(self):
        return clean_string(self._extract_provenance_date_entree()[1])  # self.observations

    @property
    def nb_exemplaire_supp(self):
        return ""

    @property
    def verified_and_present(self):
        return clean_string(self.verification_effectuee_en_2022.lower()) == "oui"

    def extract_book_reference(self) \
            -> ReferenceBibliographiqueLivre2023DB:
            # -> Dict[str, Union[str, int]]:
        editeur, lieu_edition = self._extract_publisher_and_publication_place()

        ref = ReferenceBibliographiqueLivre2023DB()
        ref.titre = clean_string(self.titre)
        ref.editeur = clean_string(editeur)
        ref.lieu_edition = clean_string(lieu_edition)
        ref.annee = self.annee_edition
        ref.nb_page = self.page_number
        ref.origin = "import"
        ref.description = clean_string(self.help_description)
        return ref
        # book_reference = {}
        # book_reference["auteurs"] = self.extract_authors()
        # book_reference["titre"] = self.titre
        # book_reference["editeur"], book_reference["lieu_edition"] = self._extract_publisher_and_publication_place()
        # book_reference["annee"] = self.annee_edition
        # book_reference["nb_page"] = self.page_number
        # book_reference["description"] = self.help_description
        #
        # return book_reference

    def extract_book_record(self) \
            -> Enregistrement2023DB:
            # -> Dict[str, str]:
        now = datetime.datetime.now()
        rec = Enregistrement2023DB()

        rec.origin = "import"
        rec.annee_obtention = self.annee_obtention
        rec.observations = clean_string(self.observations)
        rec.cote = clean_string(self.cote)
        rec.date_derniere_modification = now
        rec.row = self.row
        rec.provenance = clean_string(self.provenance)
        rec.commentaire = ""
        rec.aide_a_la_recherche = clean_string(self.aide_a_la_recherche)
        return rec

        # book_record = {}
        # book_record["reference"] = self.book_reference
        # book_record["annee_obtention"] = self.annee_obtention
        # book_record["observations"] = self.observations
        # book_record["commentaire"] = ""
        # book_record["aide_a_la_recherche"] = self.aide_a_la_recherche
        # book_record["provenance"] = self.provenance
        # book_record["cote"] = self.cote
        # book_record["nb_exemplaire_supp"] = self.nb_exemplaire_supp
        # book_record["row"] = self.row
        # return book_record

    def __repr__(self):
        return f"<Catalogue2023Row> {self.to_csv_row()}"
# endregion

# region catalogue 2025
class Catalogue2025:
    # COLUMNS = ["Cote", "Titre", "Auteurs", "Année d'édition", "Editeur", "Lieu d'édition",
    #            "Observations", "Provenance", "Date d'entrée",
    #            "Entrée bibliothèque", "Aide à la recherche"]
    COLUMNS = ["Cote", "Titre", "Auteurs", "Année d'édition", "Editeur", "Lieu d'édition",
               "Observations", "Provenance", "Date d'entrée",
               "Aide à la recherche"]
    # COLUMNS_WIDTHS = [12.55, 22, 19.36, 15, 25.55, 17.55, 29.36, 15, 16.55, 17, 62.73]  # , 8.82, 10.36]
    COLUMNS_WIDTHS = [12.55, 22, 19.36, 20, 25.55, 17.55, 29.36, 15, 16.55, 62.73]  # , 8.82, 10.36]

    def __init__(self):
        self.rows: List[Catalogue2025Row] = []
        self.column_names = []
        self.d = defaultdict(list)

    def check_column_names(self) -> Optional[List]:
        """

        :return:
        """
        match_ids = []
        # print(f"self.column_names={self.column_names}")
        for column_name in self.COLUMNS:
            if column_name in self.column_names:
                match_ids.append(self.column_names.index(column_name))
            else:
                print(f"{column_name} was not found in import file")
                return [f"{column_name} missing"]
        return match_ids

    def __repr__(self):
        return f"<Catalogue2025> {len(self.rows)} rows"

class Catalogue2025Row:

    def __init__(self, row: Enregistrement2023DB):
        self.row = row


    # @classmethod
    # def create_row_from_db(cls, row: Enregistrement2023DB):
    #     row_2023 = cls()
    #     row_2023.cote = row.cote
    #     assert row.reference is ReferenceBibliographiqueLivre2023DB
    #     row_2023.titre = row.reference.titre
    #     row_2023.auteurs =
    #     row_2023.annee_edition = row.reference.annee
    #     row_2023.editeur_lieu_edition = f"{row.reference.editeur}({row.reference.lieu_edition})"
    #     row_2023.provenance_date_entree = row[cls.PROVENANCE_DATE_ENTREE_INDEX]
    #     row_2023.help_description = row.commentaire
    #     row_2023.entree_bibliotheque = row.annee_obtention
    #     row_2023.aide_a_la_recherche = row.aide_a_la_recherche
    #     row_2023.observations = row.observations
    #     # row_2023.ouvrages_supprimes_2022 = row[cls.OUVRAGES_SUPPRIMES_INDEX]
    #     # row_2023.help_contenu_schweiz = row[cls.HELP_CONTENU_SCHWEIZ_INDEX]
    #     # row_2023.verification_effectuee_en_2022 = row[cls.VERIFICATION_2022_INDEX]
    #     return row_2023

    def to_raw_row(self) -> List[str]:
        return [
            self.row.cote,
            self.row.reference.titre if self.row.reference else "",
            ", ".join([author.first_name + " " + author.family_name for author in self.row.reference.authors]) if self.row.reference else "",
            self.row.reference.annee if self.row.reference else "",
            self.row.reference.editeur if self.row.reference else "",
            self.row.reference.lieu_edition if self.row.reference else "",
            self.row.observations,
            self.row.provenance,
            self.row.annee_obtention,
            # "",
            self.row.aide_a_la_recherche,
            # self.row.ark_name,
            # self.row.reference.nb_page,

            # self.row.description,
            # self.row.commentaire,
            # self.row.reference.origin,
            # self.row.reference.description,

            # self.row.ouvrages_supprimes_2022,
            # self.row.provenance_date_entree,
            # self.row.help_description,
            # self.row.entree_bibliotheque,
            # self.row.aide_a_la_recherche,
            # self.row.help_contenu_schweitz,
            # self.row.verification_effectuee_en_2022
        ]

    def __repr__(self):
        return f"<Catalogue2025Row> {self.row}"
# endregion

class CatalogueConverter:

    @staticmethod
    def from_schweitz_to_hamelain_1(catalogue: CatalogueSchweitz):
        export_catalogue = CatalogueHamelain1()
        for old_row in catalogue.rows:
            assert isinstance(old_row, CatalogueSchweitzRow)
            new_row = CatalogueHamelain1Row()
            new_row.cote = old_row.cote
            new_row.titre, new_row.auteurs, new_row.annee_publication, \
                new_row.editeur, new_row.nb_pages, description = \
                old_row.extract_from_auteurs_titres_editeurs_annee()
            if old_row.nb_ex_sup:
                new_row.observations += f" {old_row.nb_ex_sup} "
            if old_row.observation_transfert_bht:
                new_row.observations += f" {old_row.observation_transfert_bht} "
            if old_row.lieu_personnage:
                new_row.aide_a_la_recherche += f" {old_row.lieu_personnage} "
            if old_row.mot_clef_1:
                new_row.aide_a_la_recherche += f" {old_row.mot_clef_1} "
            if old_row.mot_clef_2:
                new_row.aide_a_la_recherche += f" {old_row.mot_clef_2} "

            export_catalogue.rows.append(new_row)

        return export_catalogue

    @staticmethod
    def from_h1_and_h2_to_h3(ch1: CatalogueHamelain1, ch2: CatalogueHamelain2) -> CatalogueHamelain3:
        # to_check_later = []
        ch3 = CatalogueHamelain3()

        print(len(set(ch1.keys())), len(set(ch2.keys())))
        common_cotes = sorted(list(set(ch1.keys()).intersection(ch2.keys())))
        only_ch1_cotes = sorted(list(set(ch1.keys()).difference(ch2.keys())))
        only_ch2_cotes = sorted(list(set(ch2.keys()).difference(ch1.keys())))
        # print("ch1")
        # print(only_ch1_cotes)
        # print("ch2")
        # print(only_ch2_cotes)
        for cote in common_cotes:
            if len(ch1.d[cote]) == 1 and len(ch2.d[cote]) == 1:
                row_3 = CatalogueHamelain3Row()
                row_1 = ch1.rows[ch1.d[cote][0]]
                row_2 = ch2.rows[ch2.d[cote][0]]

                row_3.cote = row_1.cote
                row_3.titre = row_1.titre
                row_3.auteurs = row_1.auteurs
                row_3.annee_edition = row_1.annee_publication
                row_3.editeur_lieu_edition = f"{row_1.editeur} ({row_2.lieu_edition})"
                row_3.provenance = row_2.provenance
                row_3.description = row_2.description
                row_3.entree_bibliotheque = row_2.entree_bibliotheque
                row_3.aide_a_la_recherche = row_1.aide_a_la_recherche
                row_3.observations = row_1.observations
                row_3.contenu_schweitz = row_2.contenu_schweitz
                row_3.ouvrages_desherbes = row_2.ouvrages_desherbes_2022

                ch3.rows.append(row_3)
            else:
                # from row 1
                for j in ch1.d[cote]:
                    row_1 = ch1.rows[j]
                    if row_1.cote.startswith("MM"):
                        print("oohhh")

                    row_3 = CatalogueHamelain3Row()
                    row_3.cote = f"{row_1.cote}-ATTENTION"
                    row_3.titre = row_1.titre
                    row_3.auteurs = row_1.auteurs
                    row_3.annee_edition = row_1.annee_publication
                    row_3.editeur_lieu_edition = f"{row_1.editeur}(manquant dans cette ligne)"
                    row_3.provenance = "manquant dans cette ligne"
                    row_3.description = "manquant dans cette ligne"
                    row_3.entree_bibliotheque = "manquant dans cette ligne"
                    row_3.aide_a_la_recherche = row_1.aide_a_la_recherche
                    row_3.observations = row_1.observations
                    row_3.contenu_schweitz = "manquant dans cette ligne"
                    row_3.ouvrages_desherbes = "manquant dans cette ligne"

                    ch3.rows.append(row_3)

                # from row 2
                for j in ch2.d[cote]:
                    row_2 = ch2.rows[j]

                    row_3 = CatalogueHamelain3Row()
                    row_3.cote = f"{row_2.cote}-ATTENTION"
                    row_3.titre = row_2.titre
                    row_3.auteurs = row_2.auteurs
                    row_3.annee_edition = row_2.annee_publication
                    row_3.editeur_lieu_edition = f"{row_2.editeur} ({row_2.lieu_edition})"
                    row_3.provenance = row_2.provenance
                    row_3.description = row_2.description
                    row_3.entree_bibliotheque = row_2.entree_bibliotheque
                    row_3.aide_a_la_recherche = "manquant dans cette ligne"
                    row_3.observations = "manquant dans cette ligne"
                    row_3.contenu_schweitz = row_2.contenu_schweitz
                    row_3.ouvrages_desherbes = row_2.ouvrages_desherbes_2022

                    ch3.rows.append(row_3)
        for cote in only_ch1_cotes:
            for j in ch1.d[cote]:
                row_1 = ch1.rows[j]

                row_3 = CatalogueHamelain3Row()
                row_3.cote = f"{row_1.cote}-ATTENTION"
                row_3.titre = row_1.titre
                row_3.auteurs = row_1.auteurs
                row_3.annee_edition = row_1.annee_publication
                row_3.editeur_lieu_edition = f"{row_1.editeur}(manquant dans cette ligne)"
                row_3.provenance = "manquant dans cette ligne"
                row_3.description = "manquant dans cette ligne"
                row_3.entree_bibliotheque = "manquant dans cette ligne"
                row_3.aide_a_la_recherche = row_1.aide_a_la_recherche
                row_3.observations = row_1.observations
                row_3.contenu_schweitz = "manquant dans cette ligne"
                row_3.ouvrages_desherbes = "manquant dans cette ligne"

                ch3.rows.append(row_3)
        for cote in only_ch2_cotes:
            for j in ch2.d[cote]:
                row_2 = ch2.rows[j]

                row_3 = CatalogueHamelain3Row()
                row_3.cote = f"{row_2.cote}-ATTENTION"
                row_3.titre = row_2.titre
                row_3.auteurs = row_2.auteurs
                row_3.annee_edition = row_2.annee_publication
                row_3.editeur_lieu_edition = f"{row_2.editeur} ({row_2.lieu_edition})"
                row_3.provenance = row_2.provenance
                row_3.description = row_2.description
                row_3.entree_bibliotheque = row_2.entree_bibliotheque
                row_3.aide_a_la_recherche = "manquant dans cette ligne"
                row_3.observations = "manquant dans cette ligne"
                row_3.contenu_schweitz = row_2.contenu_schweitz
                row_3.ouvrages_desherbes = row_2.ouvrages_desherbes_2022

                ch3.rows.append(row_3)
        # print(f"1-cote {cote}", ch1.d[cote], [ch1.rows[j].titre for j in ch1.d[cote]])
        # print(f"2-cote {cote}", ch2.d[cote], [ch2.rows[j].titre for j in ch2.d[cote]])
        # to_check_later.append(cote)
        return ch3


