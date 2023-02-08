from flask_cors import CORS


def setup_cors(app):
    CORS(app, supports_credentials=True)
    return app
