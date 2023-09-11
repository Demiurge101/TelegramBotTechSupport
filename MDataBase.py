import pymysql

class Database:
    "Base class for Database"
    host = "localhost"
    user = "root"

    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name

    def __del__(self):
        self.close_connect()

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=3306,
                user=self.user,
                password=self.password,
                database=self.db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"success {self.db_name}")
        except Exception as ex:
            print(f"Connection refused {self.db_name}")
            print(ex)

    def exe_query(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

class DatabaseTS(Database):
    "Database class for TechSupport"
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

    def is_content(self, key):
        with self.connection.cursor() as cursor:
            cursor.execute(f"select is_content from pathdir, map where pathdir.id_map = map.id and map.key_val = \"{key}\"")
            res = cursor.fetchall()
            for i in res:
                if i['is_content'] == True:
                    return True
            return False
    def exe_queryPath(self, key):
        with self.connection.cursor() as cursor:
            if not self.is_content(key):
                return None
            cursor.execute(f"select dir from pathdir, map where pathdir.id_map = map.id and map.key_val = \"{key}\"")
            res = cursor.fetchall()
            return res
    def close_connect(self):
        self.connection.close()

class DatabaseAuthSon(Database):
    "Database class for authorization system one number"
    def check_user(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"select * from users where user_id = {user_id}")
            res = cursor.fetchall()
            return True if len(res) == 1 else False

    def add_user(self, order_key, user_id, user_name):
        with self.connection.cursor() as cursor:
            cursor.execute(f"select id from clients where order_key = \"{order_key}\"")
            res = cursor.fetchall()
            if len(res) == 1:
                try:
                    cursor.execute(f"insert into users(org_id, user_id, user_name) value({res[0]['id']}, {user_id}, \"{user_name}\")")
                    self.connection.commit()
                    return True
                except Exception as ex:
                    print("Add user error")
                    print(ex)
                    return False
            return False

    def del_user(self, user_id):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(f"delete from users where user_id = {user_id}")
                self.connection.commit()
                return True
            except Exception as ex:
                print("delete user error")
                print(ex)
                return False
            return False

    def close_connect(self):
        self.connection.close()