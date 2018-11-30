from flask import Flask


def init_app():
    """Initialize the Flask application.

    Returns:
        Flask: The Flask application object
    """
    application = Flask(__name__)
    return application

app = init_app()
