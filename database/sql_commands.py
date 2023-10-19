import sqlite3
from database import sql_queries


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("db.sqlite3")
        self.cursor = self.conn.cursor()

    def sql_create_tables(self):
        if self.conn:
            print("Db connected successfully")

        self.conn.execute(sql_queries.CREATE_USER_TABLE_QUERY)
        self.conn.execute(sql_queries.CREATE_BAN_USER_TABLE_QUERY)

        self.conn.commit()

    def sql_insert_user_query(self, telegram_id, username, first_name, last_name):
        self.cursor.execute(
            sql_queries.INSERT_USER_QUERY,
            (None, telegram_id, username, first_name, last_name)
        )
        self.conn.commit()

    def sql_select_all_user_query(self):
        self.cursor.row_factory = lambda cursor, row: {
            'id': row[0],
            'telegram_id': row[1],
            'username': row[2],
            'first_name': row[3],
            'last_name': row[4],
        }
        return self.cursor.execute(
            sql_queries.SELECT_ALL_USER_QUERY
        ).fetchall()

    def sql_insert_ban_user_query(self, telegram_id, username):
        self.cursor.execute(
            sql_queries.INSERT_BAN_USER_QUERY,
            (None, telegram_id, username, 1)
        )
        self.conn.commit()

    def sql_update_ban_user_query(self, telegram_id):
        self.cursor.execute(
            sql_queries.UPDATE_BAN_USER_COUNT_QUERY,
            (telegram_id,)
        )
        self.conn.commit()

    def sql_select_user_query(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            'id': row[0],
            'telegram_id': row[1],
            'username': row[2],
            'first_name': row[3],
            'last_name': row[4],
        }
        return self.cursor.execute(
            sql_queries.SELECT_USER_QUERY,
            (telegram_id,)
        ).fetchall()

    def sql_select_ban_users(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            'id': row[0],
            'telegram_id': row[1],
            'username': row[2],
            'count': row[3]

        }
        return self.cursor.execute(
            sql_queries.SELECT_BAN_USER,
            (telegram_id,)
        ).fetchall()
