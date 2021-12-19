from os import path
from configparser import ConfigParser

BASE_DIR = path.abspath(path.dirname(__file__))
cpath = path.join(BASE_DIR, "../../lnkmngr_config.ini")


config = ConfigParser()
config.read(cpath)


def get_db_path_override():
    return config.get("default", "db_path_override", fallback=None)


def get_port():
    return config.getint("default", "port", fallback=5001)


def get_expose_to_lan():
    return config.getboolean("default", "expose_to_lan", fallback=False)
