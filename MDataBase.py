import pymysql

class Database:
    "Database class"
    host = "localhost"
    user = "root"

    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host = self.host,
                port = 3306,
                user = self.user,
                password = self.password,
                database= self.db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("success")
        except Exception as ex:
            print("Connection refused")
            print(ex)

    def exe_query(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()
    def map_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from map")
            rows = cursor.fetchall()
            return rows
    def set_key_text(self, key, text):
        with self.connection.cursor() as cursor:
            cursor.execute(f"insert into map(key_val,text_val) value(\"{key}\",\"{text}\");")
            self.connection.commit()
    def update_text(self, key, text):
        with self.connection.cursor() as cursor:
            cursor.execute(f"update map set text_val = \"{text}\" where key_val = \"{key}\"")
            self.connection.commit()
    def delete_text(self, key):
        with self.connection.cursor() as cursor:
            cursor.execute(f"delete from map where key_val =\"{key}\"")
            self.connection.commit()

    def exe_queryKey(self, key):
        with self.connection.cursor() as cursor:
            cursor.execute(f"select text_val from map where key_val = \"{key}\"")
            res = cursor.fetchall()
            return res[0]['text_val']

    def exe_queryPath(self, key):
        with self.connection.cursor() as cursor:
            cursor.execute(f"select dir from pathdir, map where pathdir.id_map = map.id and map.key_val = \"{key}\"")
            res = cursor.fetchall()
            return res
    def close_connect(self):
        self.connection.close()