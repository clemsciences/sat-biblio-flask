"""
Statistiques agrégées sur le catalogue.

Fournit les données nécessaires au tableau de bord des statistiques :
- histogramme des années d'obtention (les années non définies sont ignorées) ;
- histogramme des années de publication ;
- répartition des enregistrements par préfixe de cote.
"""
import re
from collections import Counter

from sat_biblio_server import sat_biblio
from sat_biblio_server.data.gazetteer import lookup_place
from sat_biblio_server.database import db, Enregistrement2023DB, ReferenceBibliographiqueLivre2023DB
from sat_biblio_server.utils import json_result

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def _extract_year(value, min_year=1400, max_year=2100):
    """Extrait la première année (nombre à 4 chiffres plausible) d'un texte libre.

    Les champs d'année sont stockés en texte (ex. "s. d.", "achat 12.06.2012") :
    on en tire une année exploitable, ou ``None`` si aucune n'est trouvée.
    """
    if value is None:
        return None
    for match in re.findall(r"\d{4}", str(value)):
        year = int(match)
        if min_year <= year <= max_year:
            return year
    return None


@sat_biblio.route("/statistics/catalogue/", methods=["GET"])
def catalogue_statistics():
    # Années d'obtention — on ignore les valeurs non définies / non exploitables.
    acquisition_counter = Counter()
    for (annee_obtention,) in db.session.query(Enregistrement2023DB.annee_obtention).all():
        year = _extract_year(annee_obtention)
        if year is not None:
            acquisition_counter[year] += 1

    # Années de publication.
    publication_counter = Counter()
    for (annee,) in db.session.query(ReferenceBibliographiqueLivre2023DB.annee).all():
        year = _extract_year(annee)
        if year is not None:
            publication_counter[year] += 1

    # Lieux de publication localisés (via le gazetteer statique).
    place_counter = Counter()
    place_coords = {}
    located_total = 0
    unlocated_total = 0
    for (lieu_edition,) in db.session.query(ReferenceBibliographiqueLivre2023DB.lieu_edition).all():
        found = lookup_place(lieu_edition)
        if found is None:
            if lieu_edition and lieu_edition.strip():
                unlocated_total += 1
            continue
        name, lat, lon = found
        place_counter[name] += 1
        place_coords[name] = (lat, lon)
        located_total += 1

    # Répartition par cote (regroupée par préfixe de cote).
    cote_counter = Counter()
    for (cote,) in db.session.query(Enregistrement2023DB.cote).all():
        if not cote or not cote.strip():
            continue
        match = re.match(r"[A-Za-z]+", cote.strip())
        prefix = match.group(0).upper() if match else "(sans préfixe)"
        cote_counter[prefix] += 1

    acquisition_years = [{"year": y, "count": c} for y, c in sorted(acquisition_counter.items())]
    publication_years = [{"year": y, "count": c} for y, c in sorted(publication_counter.items())]
    cotes = [{"prefix": p, "count": c}
             for p, c in sorted(cote_counter.items(), key=lambda kv: (-kv[1], kv[0]))]

    publication_places = [
        {"place": name, "count": c, "lat": place_coords[name][0], "lon": place_coords[name][1]}
        for name, c in sorted(place_counter.items(), key=lambda kv: (-kv[1], kv[0]))
    ]

    return json_result(True,
                       acquisition_years=acquisition_years,
                       publication_years=publication_years,
                       cotes=cotes,
                       publication_places=publication_places,
                       publication_places_located=located_total,
                       publication_places_unlocated=unlocated_total), 200
