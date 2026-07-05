"""
Gazetteer statique : nom de lieu d'édition -> coordonnées (latitude, longitude).

Le champ `lieu_edition` est du texte libre. Plutôt que de géocoder en ligne à
chaque requête, on maintient ici une table des lieux les plus fréquents du
catalogue (couvre la grande majorité des références).

Les clés sont normalisées via :func:`normalize_place` (minuscules, sans accents
superflus retirés, tirets remplacés par des espaces, point final supprimé).
"""
import re

# Coordonnées (lat, lon) des lieux d'édition connus.
# La clé de recherche est la forme normalisée du nom.
_PLACES = {
    "Paris": (48.8566, 2.3522),
    "Tours": (47.3941, 0.6848),
    "Chambray-lès-Tours": (47.3400, 0.7050),
    "Chambray": (47.3400, 0.7050),
    "Orléans": (47.9029, 1.9093),
    "Poitiers": (46.5802, 0.3404),
    "Blois": (47.5861, 1.3359),
    "Chinon": (47.1670, 0.2416),
    "Rennes": (48.1173, -1.6778),
    "Joué-lès-Tours": (47.3500, 0.6600),
    "Angers": (47.4784, -0.5632),
    "Vendôme": (47.7930, 1.0660),
    "Le Mans": (48.0061, 0.1996),
    "Saint-Cyr-sur-Loire": (47.4100, 0.6700),
    "Loches": (47.1289, 0.9955),
    "Lyon": (45.7640, 4.8357),
    "Bruxelles": (50.8503, 4.3517),
    "La Crèche": (46.3667, -0.3000),
    "Bourges": (47.0810, 2.3987),
    "Toulouse": (43.6047, 1.4442),
    "Saint-Avertin": (47.3700, 0.7200),
    "Marseille": (43.2965, 5.3698),
    "Châteauroux": (46.8110, 1.6900),
    "Amboise": (47.4130, 0.9821),
    "Nantes": (47.2184, -1.5536),
    "Saumur": (47.2600, -0.0770),
    "Caen": (49.1829, -0.3707),
    "Londres": (51.5074, -0.1278),
    "Bordeaux": (44.8378, -0.5792),
    "Genève": (46.2044, 6.1432),
    "Amsterdam": (52.3676, 4.9041),
    "Niort": (46.3239, -0.4600),
    "La Pierre-qui-Vire": (47.3200, 4.0700),
    "La Riche": (47.3900, 0.6600),
    "Lille": (50.6292, 3.0573),
    "Chartres": (48.4470, 1.4890),
    "Bléré": (47.3260, 0.9900),
    "Roanne": (46.0340, 4.0680),
    "Chemillé-sur-Indrois": (47.1600, 1.1600),
    "Chauvigny": (46.5680, 0.6480),
    "Langeais": (47.3250, 0.4030),
    "Cholet": (47.0600, -0.8790),
    "Nogent-le-Rotrou": (48.3220, 0.8200),
    "Strasbourg": (48.5734, 7.7521),
    "Ballan-Miré": (47.3500, 0.6300),
    "Laval": (48.0700, -0.7700),
    "Loudun": (47.0090, 0.0820),
    "Clermont-Ferrand": (45.7772, 3.0870),
    "La Flèche": (47.6970, -0.0740),
    "Buzançais": (46.8900, 1.4200),
    "Montrichard": (47.3430, 1.1770),
    "Issoudun": (46.9490, 1.9930),
    "Grenoble": (45.1885, 5.7245),
    "Monts": (47.2800, 0.6400),
    "Fontenay-le-Comte": (46.4670, -0.8060),
    "Dijon": (47.3220, 5.0415),
    "Amiens": (49.8940, 2.2958),
    "Montreuil-Bellay": (47.1330, -0.1520),
    "Mayenne": (48.3000, -0.6170),
    "Colmar": (48.0800, 7.3600),
    "Bourgueil": (47.2830, 0.1650),
    "Maulévrier": (47.0000, -0.7400),
    "Rouen": (49.4432, 1.0993),
    "Nancy": (48.6921, 6.1844),
}


def normalize_place(value):
    """Normalise un nom de lieu pour la recherche dans le gazetteer."""
    if value is None:
        return ""
    s = str(value).strip().rstrip(".").strip().lower()
    s = s.replace("’", "'")
    s = s.replace("-", " ")
    s = re.sub(r"\s+", " ", s)
    return s


# Table de recherche indexée par forme normalisée -> (nom d'affichage, lat, lon).
GAZETTEER = {
    normalize_place(name): (name, lat, lon)
    for name, (lat, lon) in _PLACES.items()
}


def lookup_place(value):
    """Renvoie ``(nom, lat, lon)`` pour un lieu connu, sinon ``None``."""
    return GAZETTEER.get(normalize_place(value))
