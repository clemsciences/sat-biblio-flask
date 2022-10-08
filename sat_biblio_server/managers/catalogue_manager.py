"""

"""
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


class CatalogueHamelain1:
    COLUMNS = ["Cote SAT de l'ouvrage", "Titre de l'ouvrage", "Auteur", "Année de publication", "Editeur",
               "Nombre de pages", "Entrée dans la bibliothèque", "Observations",
               "Aide à la recherche"]

    def __init__(self):
        self.rows: List[CatalogueHamelain1Row] = []

    def parse_rows(self, rows):
        for row in rows:
            hamelain_1_row = CatalogueHamelain1Row()
            hamelain_1_row.parse_row(row)
            self.rows.append(hamelain_1_row)


class CatalogueHamelain1Row:

    def __init__(self):
        self.cote = ""
        self.titre = ""
        self.auteurs = 0
        self.annee_publication = ""
        self.editeur = ""
        self.nb_pages = ""
        self.entree_bibliotheque = ""
        self.observations = ""
        self.aide_a_la_recherche = ""

    def parse_row(self, row):
        self.cote = row[0]
        self.titre = row[1]
        self.auteurs = row[2]
        self.annee_publication = row[3]
        self.editeur = row[4]
        self.nb_pages = row[5]
        self.entree_bibliotheque = row[6]
        self.observations = row[7]
        self.aide_a_la_recherche = row[8]

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
