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
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
        except Exception as e:
            print(e)

    def commit(self, cmd, err="commit error"):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(cmd)
                self.connection.commit()
                return True
            except Exception as ex:
                print(cmd)
                print(err)
                print(ex)
                return False
            return False

    def fetchall(self, cmd, err="fetch error"):
         with self.connection.cursor() as cursor:
            try:
                cursor.execute(cmd)
                return cursor.fetchall()
            except Exception as ex:
                print(cmd)
                print(err)
                print(ex)
                return {}
            return {}

    def close_connect(self):
        self.connection.close()








class DatabaseTS(Database):
    "Database class for TechSupport"
    def map_table(self):
        return self.fetchall("select * from map")
        
    def set_key_text(self, key, text):
        self.commit(f"insert into map(key_val,text_val) value(\"{key}\",\"{text}\");")

    def update_text(self, key, text):
        self.commit(f"update map set text_val = \"{text}\" where key_val = \"{key}\"")
        
    def delete_text(self, key):
        self.commit(f"delete from map where key_val =\"{key}\"")

    def exe_queryKey(self, key):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(f"select text_val from map where key_val = \"{key}\"")
                res = cursor.fetchall()
                return res[0]['text_val']
            except Exception as e:
                print(e)

    def is_content(self, key):
        res = self.fetchall(f"select is_content from pathdir, map where pathdir.id_map = map.id and map.key_val = \"{key}\"")
        for i in res:
            if i['is_content'] == True:
                return True
        return False
        
    def exe_queryPath(self, key):
        if not self.is_content(key):
            return None
        return self.fetchall(f"select dir from pathdir, map where pathdir.id_map = map.id and map.key_val = \"{key}\"")




class SonDB(Database):
    """Database for SON"""
    dblocation = "C:\\Users\\Gen\\Projects\\work\\TelegramBotTechSupport\\fileDB"

    def check_user(self, user_id):
        res = self.fetchall(f"select * from users where user_id = {user_id}")
        return True if len(res) == 1 else False

    def add_user(self, order_key, user_id, user_name):
        res = self.fetchall(f"select id from clients where order_key = \"{order_key}\"")
        if len(res) == 1:
            self.commit(f"insert into users(org_id, user_id, user_name) value({res[0]['id']}, {user_id}, \"{user_name}\")")
            return True
        return False

    def del_user(self, user_id):
        self.commit(f"delete from users where user_id = {user_id}")
                

    def addStation(self, serial_id, org_name, mkcb, date, location, description=""):
        org_id = self.getOrgIdByName(org_name) # org_id
        if org_id < 0:
            print("There is no organizations with this name!")
            return
        if len(self.fetchall(f"select * from stations where serial_number = {serial_id}")) == 1:
            print("This station already exist!")
            return
        self.commit(f"insert into stations(serial_number, org_id, mkcb, date_out, location, description_) \
            value({serial_id}, {org_id}, \"{mkcb}\", \"{date}\", \"{location}\", \"{description}\")")

    def addDevice(self, serial_id, station_id, org_name, name, mkcb, date, path, description):
        org_id = self.getOrgIdByName(org_name) # org_id
        if org_id < 0:
            print("There is no organizations with this name!")
            return
        if len(self.fetchall(f"select * from devices where serial_number = {serial_id}")) == 1:
            print("This device already exist!")
            return
        self.commit(f"insert into devices(serial_number, station_number, org_id, device_name, mkcb, date_out, location, description_) \
            value({serial_id}, {station_id}, {org_id},  \"{name}\", \"{mkcb}\", \"{date}\", \"{path}\", \"{description}\")", \
            "insert")

    def getDevices(self, serial_number, client_id):
        res = self.fetchall(f"select * from devices where serial_number = {serial_number}")
        org_id = self.fetchall(f"select org_id from users where user_id ={client_id}")
        if (len(res) == 1) and (len(org_id) == 1):
            if res[0]['org_id'] == int(org_id[0]['org_id']):
                return res[0]
        return {}

    def getStations(self, serial_number, client_id):
        res = self.fetchall(f"select * from stations where serial_number = {serial_number}")
        org_id = self.fetchall(f"select org_id from users where user_id ={client_id}")
        if (len(res) == 1) and (len(org_id) == 1):
            if res[0]['org_id'] == int(org_id[0]['org_id']):
                return res[0]
                # devices = self.fetchall(f"select * from devices where station_number = {res[0]['serial_number']}")
                # return devices
        return {}

    def deleteDevice(self, serial_number, tp="device"):
        self.commit(f"delete from {tp}s where serial_number = {serial_number}", "delete <serial_number> error")

    def delStation(self, serial_number):
        deleteDevice(serial_number, "station")

    def getOrgIdByName(self, name):
        res = self.fetchall(f"select id from clients where org = \"{name}\"")
        # print("org_id = ", res)
        if len(res) == 1:
            return res[0]['id']
        else:
            return -1

    def test(self, serial_number, client_id):
        print(" For serial_number ", serial_number, "and client_id ", client_id)
        stations = self.fetchall(f"select * from stations where serial_number = {serial_number}")
        devices = self.fetchall(f"select * from devices where serial_number = {serial_number}")
        org_id = self.fetchall(f"select org_id from users where user_id ={client_id}")
        print()
        print(stations)
        print()
        print(devices)
        print()
        print(org_id)
        