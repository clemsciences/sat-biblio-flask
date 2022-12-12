"""
This module is to code faster simple REST API.
"""

from sat_biblio_server.routes import *


@sat_biblio.route("/things/", methods=["GET", "POST"])
def published_works_list_request():
    if request.method == "GET":

        return json_result(True, ), 200
    elif request.method == "POST":

        session.close()
        return json_result(True, ), 200
    return json_result(False), 304


@sat_biblio.route("/things/<int:id_>", methods=["GET", "UPDATE", ])
def published_work_request(id_):
    if request.method == "GET":

        return json_result(True)
    elif request.method == "UPDATE":

        return json_result(True)
    return json_result(False), 304


