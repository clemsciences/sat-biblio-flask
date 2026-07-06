"""

"""


def get_pagination(r):
    n_page = int(r.args.get("page", "1"))
    size = int(r.args.get("size", "50"))
    sort_by = r.args.get("sortBy", "").strip()
    sort_desc = r.args.get("sortDesc", "false").lower() in ["true", "1", "t", "y", "yes"]
    return n_page, size, sort_by, sort_desc


def int_to_bool(query):
    if query == "1":
        return True
    elif query == "0":
        return False
    else:
        raise ValueError


def get_current_user_id():
    """
    Identifiant de l'utilisateur courant, pour tracer l'auteur d'un événement.

    L'authentification se fait principalement par JWT (Bearer) et, en repli,
    par session Flask. On lit donc le JWT en priorité (claim « id » si présent,
    sinon l'identité = email résolue en base), puis la session.
    Retourne -1 si aucun utilisateur n'est identifiable.

    Les imports sont faits localement pour éviter les imports circulaires
    (sat_biblio_server importe le paquet routes au démarrage).
    """
    from flask import session
    from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
    from sat_biblio_server import UserDB
    try:
        verify_jwt_in_request(optional=True)
        claims = get_jwt() or {}
        if claims.get("id"):
            return claims["id"]
        identity = get_jwt_identity()
        if identity:
            user = UserDB.query.filter_by(email=identity).first()
            if user:
                return user.id
    except Exception:
        pass
    return session.get("id", -1)
