import os

from flask import Flask

import db
import routes

HOST = "0.0.0.0"
PORT = 1111


def create_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__, template_folder=os.path.join(base_dir, "templates"))
    db.init_app(app)
    routes.register_routes(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host=HOST, debug=False, port=PORT)
