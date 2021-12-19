from flask import Flask
from utils.config import get_port, get_expose_to_lan


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


app = init_app()
app.run(port=get_port(), host="0.0.0.0" if get_expose_to_lan() else "")
