"""From database to Dublin Core

"""

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


def from_data_to_dublin_core(record_data, reference_data, authors_data):
    return dict(Title="",
                Creator="",
                Subject="",
                Description="",
                Publisher="",
                Contributor="",
                Date="",
                Type="",
                Format="",
                Identifier="",
                Source="",
                Language="",
                Relation="",
                Coverage="",
                Rights="")
