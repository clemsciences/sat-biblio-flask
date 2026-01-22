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
