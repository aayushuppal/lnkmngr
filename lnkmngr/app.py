from flask import Flask
from utils.config import get_port, get_expose_to_lan
from pathlib import Path
import shutil
import glob


def clean_tmp_files():
    rootdir = Path.cwd()
    tmp_mei_dirs = []
    for path in glob.glob(f"{rootdir}/_MEI*"):
        p = Path(path)
        tmp_mei_dirs.append((p, p.stat().st_mtime))
    tmp_mei_dirs = sorted(tmp_mei_dirs, key=lambda x: -x[1])
    for x in tmp_mei_dirs[2:]:
        shutil.rmtree(x[0], ignore_errors=True)


def init_app():
    app = Flask(__name__)

    app.config["FLASK_ENV"] = "development"
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_FOLDER"] = "templates"
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    with app.app_context():
        import routes

    return app


clean_tmp_files()
app = init_app()
app.run(port=get_port(), host="0.0.0.0" if get_expose_to_lan() else "")
