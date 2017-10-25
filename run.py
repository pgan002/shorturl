import importlib

from src import app


if __name__ == '__main__':
    # Import and register routes with Flask application
    importlib.import_module('.routes', 'src')

    app.run('localhost', port=8080, debug=True)
