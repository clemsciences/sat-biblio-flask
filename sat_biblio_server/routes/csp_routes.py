"""
Réception des rapports de violation de la Content-Security-Policy.

La CSP de l'interface est d'abord déployée en mode « Report-Only » : le
navigateur ne bloque rien mais envoie ici chaque ressource qui aurait été
bloquée. Ces rapports, lus dans le journal du serveur, servent à ajuster la
politique avant de l'appliquer réellement.
"""

import json
import logging

from flask import request

from sat_biblio_server import sat_biblio
from sat_biblio_server.limiter import limiter

logger = logging.getLogger("sat_biblio.csp")

# Champs utiles d'un rapport (ancien format « csp-report » et format Reporting API).
_FIELDS = ("document-uri", "documentURL", "violated-directive", "effectiveDirective",
           "blocked-uri", "blockedURL", "source-file", "sourceFile", "line-number", "lineNumber")


@sat_biblio.route("/csp-report/", methods=["POST"])
@limiter.limit("60 per hour")
def csp_report():
    try:
        payload = json.loads(request.get_data(cache=False, as_text=True)[:10_000] or "{}")
    except ValueError:
        return "", 204
    # Ancien format : {"csp-report": {...}} ; Reporting API : [{"type": "csp-violation", "body": {...}}]
    if isinstance(payload, dict):
        reports = [payload.get("csp-report", payload)]
    elif isinstance(payload, list):
        reports = [item.get("body", {}) for item in payload if isinstance(item, dict)]
    else:
        reports = []
    for report in reports[:10]:
        if isinstance(report, dict):
            summary = {k: report[k] for k in _FIELDS if k in report}
            logger.warning("Violation CSP : %s", json.dumps(summary, ensure_ascii=False)[:1000])
    return "", 204
