import re


def extraire_auteurs(description):
    prenom = ""
    nom = ""
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
        auteurs.append(dict(first_name=prenom, family_name=nom, valide=True))

    return auteurs, description[limite_auteur:]


def extraire_ref_biblio(description):
    if len(description) > 0:
        # auteur
        auteurs, reste = extraire_auteurs(description.split(","))
        i = 0
        # print("reste", reste)
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
                    if len(reste) >= i+1:
                        titre = reste[i].strip()
                        # print("titre not matched", titre)
                    else:
                        titre = ""
                i += 1
                # endregion

                # region lieu d'édition
                if len(reste) >= i+1:
                    if reste[i] == "":
                        lieu_edition = "s.l."
                    else:
                        lieu_edition = reste[i]
                else:
                    lieu_edition = ""
                i += 1
                # endregion

                # region éditeur
                if len(reste) >= i+1:
                    if reste[i] == "":
                        editeur = "s.n."
                    else:
                        editeur = reste[i]
                else:
                    editeur = ""
                # endregion

                # region nombre de pages
                if len(reste) >= i+1:
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
                    if len(reste) >= i+1:
                        titre = reste[i].strip()
                        # print("titre not matched", titre)
                    else:
                        titre = ""
                i += 1
                # endregion

                # region lieu d'édition
                if len(reste) >= i+1:
                    if reste[i] == "":
                        lieu_edition = "s.l."
                    else:
                        lieu_edition = reste[i]
                else:
                    lieu_edition = ""
                i += 1
                # endregion

                # region éditeur
                if len(reste) >= i+1:
                    if reste[i] == "":
                        editeur = "s.n."
                    else:
                        editeur = reste[i]
                else:
                    editeur = ""
                i += 1
                # endregion

                # region année
                if len(reste) >= i+1:
                    if reste[i] == "":
                        annee = "s.d."
                    else:
                        annee = reste[i]
                else:
                    annee = ""
                i += 1
                # endregion

                # region nombre de pages
                if len(reste) >= i+1:
                    if reste[i] == "":
                        nb_page = "x.p."
                    else:
                        nb_page = reste[i]
                else:
                    nb_page = ""
                i += 1
                # endregion

            ref = dict(
                authors=auteurs,
                titre=titre.strip(),
                lieu_edition=lieu_edition.strip(),
                editeur=editeur.strip(),
                annee=annee.strip(),
                nb_page=nb_page.strip(), valide=True)
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
