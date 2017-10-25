import sqlite3


class SqliteDB(object):

    def __init__(self, database_file_path):
        """Initialize the sqlite database connection.

        Args:
            database_file_path (str): Path to file where database is stored. The file will be
                created if it does not exist.
        """
        # Initialize the database connection, using sqlite3.Row as the row_factory
        self.connection = sqlite3.connect(database_file_path)
        self.connection.row_factory = sqlite3.Row

        # Store the database cursor
        self.cursor = self.connection.cursor()

    def get_connection(self):
        """Get the database connection object.

        Returns:
            sqlite3.Connection: The SQLite database connection
        """
        return self.connection

    def get_cursor(self):
        """Get the database cursor object.

        Returns:
            sqlite3.Cursor: The SQLite database cursor as returned by
                sqlite3.Connection.cursor()
        """
        return self.cursor


if __name__ == '__main__':
    db = SqliteDB('/tmp/test.db')
    cur = db.get_cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS test (id int, data text)')

    cur.execute('INSERT INTO test (id, data) VALUES (?, ?)', (1, 'foo'))
    db.get_connection().commit()

    cur.execute('SELECT * FROM test')
    rows = cur.fetchall()
    for row in rows:
        for column in row.keys():
            print('%s: %s' % (column, row[column]))
        print()
