import sqlite3

from database import sql_queries


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("db.sqlite3")
        self.cursor = self.conn.cursor()

    def sql_create_tables(self):
        if self.conn:
            print("BD connected successfully")

        self.conn.execute(sql_queries.CREATE_USER_TABLE_QUERY)
        self.conn.execute(sql_queries.CREATE_BAN_USER_TABLE_QUERY)
        self.conn.execute(sql_queries.CREATE_USER_FORM_TABLE_QUERY)
        self.conn.execute(sql_queries.CREATE_LIKE_TABLE_QUERY)
        self.conn.execute(sql_queries.CREATE_DISLIKE_TABLE_QUERY)
        self.conn.execute(sql_queries.CREATE_REFERENCE_TABLE_QUERY)
        try:
            self.conn.execute(sql_queries.ALTER_USER_TABLE)
        except sqlite3.OperationalError:
            pass
        self.conn.commit()

    def sql_insert_user_query(self, telegram_id, username, first_name, last_name):
        self.cursor.execute(
            sql_queries.INSERT_USER_QUERY,
            (None, telegram_id, username, first_name, last_name, None)
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
            'link': row[5]
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

    def sql_insert_user_form_query(self, telegram_id, nickname,
                                   bio, age, occupation, photo):
        self.cursor.execute(
            sql_queries.INSERT_USER_FORM_QUERY,
            (None, telegram_id, nickname, bio, age, occupation, photo)
        )
        self.conn.commit()

    def sql_select_user_form_query(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            'id': row[0],
            "telegram_id": row[1],
            "nickname": row[2],
            "bio": row[3],
            "age": row[4],
            "occupation": row[5],
            "photo": row[6],
        }
        return self.cursor.execute(
            sql_queries.SELECT_USER_FORM_QUERY,
            (telegram_id,)
        ).fetchall()

    def sql_select_all_user_form_query(self):
        self.cursor.row_factory = lambda cursor, row: {
            'id': row[0],
            "telegram_id": row[1],
            "nickname": row[2],
            "bio": row[3],
            "age": row[4],
            "occupation": row[5],
            "photo": row[6],
        }
        return self.cursor.execute(
            sql_queries.SELECT_ALL_USERS_FORM_QUERY,
        ).fetchall()

    def sql_insert_like_query(self, owner, liker):
        self.cursor.execute(
            sql_queries.INSERT_LIKE_QUERY,
            (None, owner, liker,)
        )
        self.conn.commit()

    def sql_insert_dislike_query(self, owner, disliker):
        self.cursor.execute(
            sql_queries.INSERT_DISLIKE_QUERY,
            (None, owner, disliker,)
        )
        self.conn.commit()

    def sql_delete_form_query(self, owner):
        self.cursor.execute(
            sql_queries.DELETE_USER_FORM_QUERY,
            (owner,)
        )
        self.conn.commit()

    def sql_update_user_form_query(self, nickname, bio, age, occupation, photo, telegram_id):
        self.cursor.execute(
            sql_queries.UPDATE_USER_FORM_QUERY,
            (nickname, bio, age, occupation, photo, telegram_id,)
        )
        self.conn.commit()


    def get_liked_users(self, liker_telegram_id):
        liked_users = []
        self.cursor.execute(
            sql_queries.SELECT_LIKER_USER,
            (liker_telegram_id,)
        )
        rows = self.cursor.fetchall()
        for row in rows:
            liked_users.append(row[0])
        return liked_users

    def get_disliked_users(self, disliker_telegram_id):
        disliked_users = []
        self.cursor.execute(
            sql_queries.SELECT_DISLIKER_USER,
            (disliker_telegram_id,)
        )
        rows = self.cursor.fetchall()
        for row in rows:
            disliked_users.append(row[0])
        return disliked_users

    def sql_insert_referral_query(self, owner, referral):
        self.cursor.execute(
            sql_queries.INSERT_REFERRAL_QUERY,
            (None, owner, referral,)
        )
        self.conn.commit()

    def sql_select_user_by_link_query(self, link):
        self.cursor.row_factory = lambda cursor, row: {
            'id': row[0],
            "telegram_id": row[1],
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "link": row[5]
        }
        return self.cursor.execute(
            sql_queries.SELECT_USER_BY_LINK_QUERY,
            (link,)
        ).fetchall()

    def sql_update_user_reference_link_query(self, link, telegram_id):
        self.cursor.execute(
            sql_queries.UPDATE_USER_REFERENCE_LINK_QUERY,
            (link, telegram_id,)
        )
        self.conn.commit()


    def sql_select_all_referral_by_owner_query(self, owner):
        self.cursor.row_factory = lambda cursor, row: {
            'id': row[0],
            "owner": row[1],
            "referral": row[2]
        }
        return self.cursor.execute(
            sql_queries.SELECT_ALL_REFERRAL_BY_OWNER_QUERY,
            (owner,)
        ).fetchall()
