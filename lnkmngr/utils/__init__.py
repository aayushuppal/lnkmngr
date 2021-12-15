def under_str_frmt(x):
    y = x.split("_")
    return " ".join(y)


def is_valid_category_id(id):
    try:
        int(id)
        return True
    except:
        return False
