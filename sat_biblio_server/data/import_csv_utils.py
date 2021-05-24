import re


def extraire_auteurs(description):
    prenom = ""
    nom = ""
    limite_auteur = 0
    auteurs = []
    while limite_auteur < len(description):
        field = description[limite_auteur]
        print("field", repr(field))
        m = re.match(r"(?P<nom>[\w\- '.]+) \((?P<prenom>[ \-'\w.]+)\)", field)
        print(m)
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
        auteurs.append(dict(first_name=prenom, family_name=nom))

    return auteurs, description[limite_auteur:]


def extraire_ref_biblio(description):
    if len(description) > 0:
        # auteur
        auteurs, reste = extraire_auteurs(description.split(","))

        if len(reste) > 0:
            # titre
            m = re.match(r"\"\"(?P<titre>\w+)\"\"", reste[0])
            if m is not None:
                titre = m.group("titre")
            else:
                if len(reste) >= 1:
                    titre = reste[0]
                else:
                    titre = ""

            # lieu d'édition
            if len(reste) >= 2:
                if reste[1] == "":
                    lieu_edition = "s.l."
                else:
                    lieu_edition = reste[1]
            else:
                lieu_edition = ""

            # éditeur
            if len(reste) >= 3:
                if reste[2] == "":
                    editeur = "s.n."
                else:
                    editeur = reste[2]
            else:
                editeur = ""

            # année
            if len(reste) >= 4:
                if reste[3] == "":
                    annee = "s.d."
                else:
                    annee = reste[3]
            else:
                annee = ""

            # nombre de pages
            if len(reste) >= 5:
                if reste[4] == "":
                    nb_page = "x.p."
                else:
                    nb_page = reste[4]
            else:
                nb_page = ""

            ref = dict(
                authors=auteurs,
                titre=titre.strip(),
                lieu_edition=lieu_edition.strip(),
                editeur=editeur.strip(),
                annee=annee.strip(),
                nb_page=nb_page.strip())
            return ref
        else:
            return None
    else:
        return None


def extraire_enregistrements(record):
    # print(record.keys())
    mots_clef = f"{record.get('theme1', '')} " \
                f"{record.get('theme2', '')} " \
                f"{record.get('theme3', '')}".strip()
    record = dict(description=record["description"], cote=record["cote"],
                  nb_exemplaire_supp=record["nb_supp"],
                  annee=record["annee"], provenance=record["provenance"],
                  mots_clef=mots_clef, valide=True, id_reference=record["index"])
    return record
