import unittest
from contextlib import closing
from time import sleep
from unittest import TestCase
import psycopg2
import pg8000
import testing.postgresql


class TestDatabase(TestCase):
    def setUp(self):
        self.postgresql = testing.postgresql.Postgresql()

    def test_create_postgresql(self):
        self.assertIsNotNone(self.postgresql)

    def test_connect_db(self):
        conn = psycopg2.connect(**self.postgresql.dsn())
        self.assertIsNotNone(conn)
        conn.close()

    def test_create_table(self):
        conn = pg8000.connect(**self.postgresql.dsn())
        with closing(conn.cursor()) as cursor:
            cursor.execute("CREATE TABLE test_tbl(id int, val text)")
            cursor.execute("INSERT INTO test_tbl values(0, 'hello'), (1, 'bye')")
            cursor.execute('SELECT * FROM test_tbl ORDER BY id')
            self.assertEqual(cursor.fetchall(), ([0, 'hello'], [1, 'bye']))
            cursor.close()
        conn.close()

    def test_stop_postgresql(self):
        postgresql = testing.postgresql.Postgresql()
        postgresql.stop()
        # sleep(3)
        self.assertFalse(postgresql.is_alive())

    def tearDown(self):
        self.postgresql.stop()


if __name__ == '__main__':
    unittest.main()
