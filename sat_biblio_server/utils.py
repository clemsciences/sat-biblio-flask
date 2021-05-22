"""

"""
import datetime
import enum

from flask import jsonify


__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class UserRight(enum.Enum):
    """
    >>> UserRight.administrateur < UserRight.lecteur
    False

    """
    lecteur = enum.auto()
    contributeur = enum.auto()
    editeur = enum.auto()
    gestionnaire = enum.auto()
    administrateur = enum.auto()

    @classmethod
    def from_value(cls, value):
        if value == cls.lecteur.value:
            return cls.lecteur
        elif value == cls.contributeur.value:
            return cls.contributeur
        elif value == cls.editeur.value:
            return cls.editeur
        elif value == cls.gestionnaire.value:
            return cls.gestionnaire
        elif value == cls.administrateur.value:
            return cls.administrateur

    def __str__(self):
        if self == UserRight.lecteur:
            return "lecteur"
        elif self == UserRight.contributeur:
            return "contributeur"
        elif self == UserRight.editeur:
            return "éditeur"
        elif self == UserRight.gestionnaire:
            return "gestionnaire"
        elif self == UserRight.administrateur:
            return "administrateur"

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return other.__le__(self)

    def __gt__(self, other):
        return other.__lt__(self)


# region TEMPS
class Date:
    def __init__(self, jour, mois, annee):
        self.jour = jour
        self.mois = mois
        self.annee = annee

    @staticmethod
    def from_html_to_date(date_str: str):
        liste_date = date_str.split("-")
        jour = int(liste_date[2])
        mois = int(liste_date[1])
        annee = int(liste_date[0])
        return datetime.date(annee, mois, jour)

    @staticmethod
    def from_string_francais(date_str: str):
        liste_date = date_str.split("/")
        jour = int(liste_date[0])
        mois = int(liste_date[1])
        annee = int(liste_date[2])
        return DateHeure(jour=jour, mois=mois, annee=annee)

    # @staticmethod
    # def from_html_to_date(date_str):
    #     liste_date = date_str.split("-")
    #     jour = int(liste_date[2])
    #     mois = int(liste_date[1])
    #     annee = int(liste_date[0])
    #     return DateHeure(jour=jour, mois=mois, annee=annee, heure=1, minute=3)

    def beau_format_jour(self):
        ajout_jour = ""
        ajout_mois = ""
        if int(self.jour) < 10:
            ajout_jour = "0" + ajout_jour
        if int(self.mois) < 10:
            ajout_mois = "0" + ajout_mois
        return ajout_jour + str(self.jour) + "/" + ajout_mois + str(self.mois) + "/" + str(self.annee)

    def format_jour_pour_fichier(self):
        ajout_jour = ""
        ajout_mois = ""
        if int(self.jour) < 10:
            ajout_jour = "0" + ajout_jour
        if int(self.mois) < 10:
            ajout_mois = "0" + ajout_mois
        return ajout_jour + str(self.jour) + "-" + ajout_mois + str(self.mois) + "-" + str(self.annee)

    def nombre_de_jours_separant(self, autre_d):
        assert isinstance(autre_d, Date)
        d1 = datetime.datetime.today()
        d2 = datetime.datetime.today()
        d1 = d1.replace(year=self.annee, month=self.mois, day=self.jour)
        d2 = d2.replace(year=autre_d.annee, month=autre_d.mois, day=autre_d.jour)
        print(d1, d2)
        return (d2 - d1).days

    def liste_jours_entre_dates(self, autre_d):
        assert isinstance(autre_d, Date)
        d1 = datetime.datetime.today()
        d2 = datetime.datetime.today()
        d1 = d1.replace(self.annee, self.mois, self.jour)
        d2 = d2.replace(autre_d.annee, autre_d.mois, autre_d.jour)
        jours = []
        for i in range(d1.toordinal(), d2.toordinal() + 1):
            ordinal = datetime.datetime.fromordinal(i)
            jours.append(Date(ordinal.day, ordinal.month, ordinal.year))
        return jours


class Heure:
    def __init__(self, heure: int, minute: int):
        # assert heure < 24
        # assert minute < 60
        self.heure = heure
        self.minute = minute

    def beau_format_heure(self):
        if int(self.minute) < 10:
            return str(self.heure) + "h0" + str(self.minute)
        else:
            return str(self.heure) + "h" + str(self.minute)


class DateHeure(Date, Heure):
    def __init__(self, heure=None, minute=None, jour=None, mois=None, annee=None):
        Date.__init__(self, jour, mois, annee)
        Heure.__init__(self, heure, minute)
        self.heure = heure
        self.minute = minute
        self.jour = jour
        self.mois = mois
        self.annee = annee

    def __str__(self):
        return datetime.datetime(int(self.annee), int(self.mois), int(self.jour),
                                 int(self.heure), int(self.minute)).strftime("%H:%M %d/%m/%Y")

    def est_anterieur(self, autre_dh):
        assert isinstance(autre_dh, DateHeure)
        if self.annee < autre_dh.annee:
            return True
        elif self.annee > autre_dh.annee:
            return False
        else:
            if self.mois < autre_dh.mois:
                return True
            elif self.mois > autre_dh.mois:
                return False
            else:
                if self.jour < autre_dh.jour:
                    return True
                elif self.jour > autre_dh.jour:
                    return False
                else:
                    if self.heure < autre_dh.heure:
                        return True
                    elif self.heure > autre_dh.heure:
                        return False
                    else:
                        return self.minute <= autre_dh.minute

    @staticmethod
    def from_select_datetime(d: dict, label: str):
        print(d)
        heure = int(d["heure_" + label])
        minute = int(d["minute_" + label])
        jour = int(d["jour_" + label])
        mois = int(d["mois_" + label])
        annee = int(d["annee_" + label])
        return datetime.datetime(int(annee), int(mois), int(jour), int(heure), int(minute))

    @staticmethod
    def from_datepicker(d: dict, label: str):
        date = d["datetimepicker-date-input-" + label]
        date_s = date.split("/")
        if len(date_s) == 3:
            jour, mois, annee = date_s
        else:
            return None
        return datetime.datetime(int(annee), int(mois), int(jour), 0, 0)

    @staticmethod
    def from_datetimepicker(d: dict, label: str):
        date = d["datetimepicker-date-input-"+label]
        date_s = date.split("/")
        if len(date_s) == 3:
            jour, mois, annee = date_s
        else:
            return None
        hour = d["datetimepicker-hour-input-"+label]
        hour_s = hour.split(":")
        if len(hour_s) == 2:
            heure, minute = hour_s
        else:
            return None
        return datetime.datetime(int(annee), int(mois), int(jour), int(heure), int(minute))

    def from_dictionary_app(self, d: dict):
        """
        De l'application Android SKILVIT vers la date_heure
        :param d:
        :return:
        """
        print(d)
        self.heure = int(d["heure"])
        self.minute = int(d["minute"])
        self.jour = int(d["jour"])
        self.mois = int(d["mois"])
        self.annee = int(d["annee"])
        return datetime.datetime(int(self.annee), int(self.mois), int(self.jour), int(self.heure), int(self.minute))

    def from_dictionary_app_label(self, d: dict, label: str):
        print(d)
        self.heure = int(d["_".join(["heure", label])])
        self.minute = int(d["_".join(["minute"])])
        self.jour = int(d["_".join(["jour"])])
        self.mois = int(d["_".join(["mois"])])
        self.annee = int(d["_".join(["annee"])])
        return datetime.datetime(int(self.annee), int(self.mois), int(self.jour), int(self.heure), int(self.minute))

    def from_view_to_date(self, d: dict):
        """
        Des vues vers la date_heure
        :param d:
        :return:
        """
        s_date = d["date_heure"]
        date, heure = s_date.split('T')
        self.annne, self.mois, self.jour = date.split("-")
        self.heure, self.minute = heure.split(":")

    @staticmethod
    def from_view_to_datetime(date_str: str):
        """
        De la vue à datetime
        :param d: {"date_heure" :
        :return:
        """
        # date_str = d["entree_date"]
        print(date_str)
        date, heure = date_str.split('T')
        annee, mois, jour = date.split("-")
        heure, minute = heure.split(":")
        return datetime.datetime(int(annee), int(mois), int(jour), int(heure), int(minute))

    @staticmethod
    def from_firefox(date_str: str):
        print(date_str)
        date, heure = date_str.split(' ')
        annee, mois, jour = date.split("-")
        heure, minute, secondes = heure.split(":")
        return datetime.datetime(int(annee), int(mois), int(jour), int(heure), int(minute), int(secondes))

    def from_dictionary_beau_format(self, d: dict):
        """

        :param d: {"heure": "00h00", "date": "00/00/00"}
        :return:
        """
        heures = d["heure"].split("h")
        if len(heures) == 2:
            heure, minute = d["heure"].split("h")
        else:
            heure = heures
            minute = 0
        jour, mois, annee = d["date"].split("/")
        self.heure = int(heure)
        self.minute = int(minute)
        self.jour = int(jour)
        self.mois = int(mois)
        self.annee = int(annee)

    def from_datetime(self, dt):
        self.heure = dt.hour
        self.minute = dt.minute
        self.annee = dt.year
        self.mois = dt.month
        self.jour = dt.day

    def to_json(self):
        return [self.annee, self.mois, self.jour, self.heure, self.minute]


# endregion


# region

def json_result(success: bool,
                message="",
                **data):
    return jsonify({"success": success,
                    "message": message,
                    **data})
