import sqlite3

from .. import app
FILE_PATH = app.config.get('DB_FILE')


class SqliteDB(object):

    def __init__(self, file_path=FILE_PATH):
        """Initialize the sqlite database connection.

        Args:
            file_path (str, optional): Path to file where database is stored.
            The file will be created if it does not exist. If not specified,
            use the file path specified in the app config.
        """
        # Initialize the db connection using sqlite3.Row as the row_factory
        self.connection = sqlite3.connect(file_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def get_url_and_token(self, id_: str):
        """Return the URL and authorization token corresponding to the given URL
        ID stored in the database, if any

        Args:
                id_ (str): URL ID
        Return:
                tuple (str, str): (URL, authorization-token) corresponding to
                the ID, or None, None if the URL ID is not in the DB
        """
        q = 'SELECT url, auth_token FROM urls WHERE id = ?'
        self.cursor.execute(q, [id_])
        rows = self.cursor.fetchall()
        if rows:
            return rows[0]  # The match is unique because `id` is a primary key
        return None, None

    def delete_url(self, id_):
        """Delete the database row corresponding to the given URL ID

        Args:
                id_ (str): URL ID
        """
        self.cursor.execute('DELETE FROM urls WHERE id = ?', [id_])
        self.connection.commit()

    def add_url(self, id_, url, token):
        """Store a database row with the given URL ID, URL and authorization
        token.

        Args:
            id_: URL ID
            url: URL
            token: Authorization token
            """
        q = 'INSERT INTO urls VALUES (?, ?, ?)'
        self.cursor.execute(q, [id_, url, token])
        self.connection.commit()

    def get_stats(self, id_):
        """Return statistics of successful redirects by the service, stored by
        method `update_stats()`.

        Args:
            id_ (str): URL ID
        Return:
            A dictionary of IP address and count of successful redirects
        """
        self.cursor.execute('SELECT ip, count FROM stats WHERE id = ?', [id_])
        return {ip: count for ip, count in self.cursor.fetchall()}

    def update_stats(self, id_, ip):
        """Record a successful URL redirect by the service.

        Args:
            id_ (str): URL ID
        """
        q = 'INSERT OR IGNORE INTO stats VALUES (?, ?, 0)'
        self.cursor.execute(q, [id_, ip])

        q = 'UPDATE stats SET count = count + 1 WHERE id = ? AND ip = ?'
        self.cursor.execute(q, [id_, ip])

        self.connection.commit()


if __name__ == '__main__':
    db = SqliteDB('/tmp/test.db')

    db.cursor.execute('CREATE TABLE IF NOT EXISTS test (id int, data text)')

    db.cursor.execute('INSERT INTO test (id, data) VALUES (?, ?)', (1, 'foo'))
    db.connection.commit()

    db.cursor.execute('SELECT * FROM test')
    rows = db.cursor.fetchall()
    for row in rows:
        for column in row.keys():
            print('%s: %s' % (column, row[column]))
        print()
