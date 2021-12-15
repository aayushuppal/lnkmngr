import os


def get_lnkmngr_db_path():
    # uncomment this to build exe with override path
    # return "C:\\Users\\auppal\\dev\\pfin2\\pfin-input-data\\sqlite_db\\lnkmngr.db"
    try:
        return os.environ["DB_PATH"]
    except KeyError:
        from os import path

        BASE_DIR = path.abspath(path.dirname(__file__))
        return path.join(BASE_DIR, "../../lnkmngr.db")


CATEGORY_TYPE = "category"
LINK_TYPE = "link"
