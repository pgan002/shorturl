import os
import importlib

from src import app


if __name__ == '__main__':
    app.config.from_pyfile(os.path.join(os.pardir, 'config.ini'))
    # Import and register routes with Flask application
    importlib.import_module('.routes', 'src')
    app.run('localhost', port=8080, debug=True)
