import os
from utils.config import get_db_path_override


def get_lnkmngr_db_path():
    db_path = get_db_path_override()
    if db_path is None:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(BASE_DIR, "../../lnkmngr.db")

    print(db_path)
    return db_path


CATEGORY_TYPE = "category"
LINK_TYPE = "link"
