"""

"""
from collections import defaultdict
import re
from typing import List


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
        print(description)
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
            auteurs.append(dict(first_name=prenom.strip(), family_name=nom.strip(), valide=True))
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
    else:
        return ""


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


class CatalogueHamelain3:
    COLUMNS = ["Cote", "Titre", "Auteur", "Année d'édition", "Editeur (lieu d'édition)",
               "Provenance", "Description", "Entrée bibliothèque",
               "Aide à la recherche", "Observations", "Contenu colonne Schweitz",
               "Ouvrages supprimés en 2022", "Vérification effectuée en 2022"]
    COLUMNS_WIDTHS = [12.55, 22, 19.36, 8, 25.55, 17.55, 29.36, 11, 16.55, 13, 62.73, 8.82, 10.36]

    def __init__(self):
        self.rows: List[CatalogueHamelain3Row] = []
        self.d = defaultdict(list)

    def parse_rows(self, rows, ignore_n_first_rows=2):
        for i, row in enumerate(rows):
            if i > ignore_n_first_rows:
                hamelain_3_row = CatalogueHamelain3Row()
                hamelain_3_row.parse_row(row)

                self.rows.append(hamelain_3_row)
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


