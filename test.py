import os
import tempfile

import unittest

print(os.getcwd())
from src import app
from src.db import sqlite
import alembic.versions


class AppTest(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.testing = True
        self.app = app.test_client()
        self.db = sqlite.SqliteDB(app.config['DATABASE'])
        with app.app_context():
            alembic.versions.0001_create_urls_table

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
        self.db = None

    def test_redirect_invalid_id(self):
        r = self.app.get('/abc')
        self.assertEqual(r.status_code, 404)

    def test_redirect_ok(self):
        self.db.add_url('abc', 'http://renew.com', 'xyz')
        r = self.app.get('/abc')
        self.assertEqual(r.status_code, 301)

    # def test_create_invalid_id(self):
    #     pass
    #
    # def test_create_id_exists(self):
    #     pass
    #
    # def test_create_id(self):
    #     pass
    #
    # def test_delete_no_auth(self):
    #     pass
    #
    # def test_delete_auth_mismatch(self):
    #     pass
    #
    # def test_delete_unknown_id(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
