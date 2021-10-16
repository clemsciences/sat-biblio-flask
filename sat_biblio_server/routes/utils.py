"""

"""


def get_pagination(r):
    n_page = int(r.args.get("page", "0"))
    size = int(r.args.get("size", "0"))
    sort_by = r.args.get("sortBy", "")
    return n_page, size, sort_by


def int_to_bool(query):
    if query == "1":
        return True
    elif query == "0":
        return False
    else:
        raise ValueError
