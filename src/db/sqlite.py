import sqlite3

from .. import app
FILE_PATH = app.config.get('DB_FILE')


class SqliteDB(object):

    def __init__(self, file_path=FILE_PATH):
        """Initialize the sqlite database connection.

        Args:
            database_file_path (str): Path to file where database is stored. The file will be
                created if it does not exist.
        """
        # Initialize the db connection using sqlite3.Row as the row_factory
        self.connection = sqlite3.connect(file_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def get_url_and_token(self, id_):
        self.cursor.execute('SELECT url, auth_token FROM urls WHERE id = ?',
                            [id_])
        rows = self.cursor.fetchall()
        if rows:
            return rows[0]  # The match is unique because `id` is a primary key
        return None, None

    def delete_url(self, id_):
        self.cursor.execute('DELETE FROM urls WHERE id = ?', [id_])
        self.connection.commit()

    def add_url(self, id_, url, token):
        q = 'INSERT INTO urls VALUES (?, ?, ?)'
        self.cursor.execute(q, [id_, url, token])
        self.connection.commit()

    def get_stats(self, id_):
        self.cursor.execute('SELECT ip, count FROM stats WHERE id = ?', [id_])
        return {ip: count for ip, count in self.cursor.fetchall()}

    def update_stats(self, id_, ip):
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
