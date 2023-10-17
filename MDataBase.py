import pymysql
import Config
from includes import *

class Database:
    "Base class for Database"
    host = "localhost"
    user = "root"

    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.__status = 1


    def set_time_out(self, tm=28800):
        self._commit(f"SET GLOBAL connect_timeout={tm}")
        self._commit(f"SET GLOBAL interactive_timeout={tm}")
        self._commit(f"SET GLOBAL wait_timeout={tm}")

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
            self.__status = 1
            print(f"success {self.db_name}")
        except Exception as ex:
            print(f"Connection refused {self.db_name}")
            print(ex)


    def _checkSlash(self, line):
        return line.replace('\\', '\\\\')

    def _checkQuote(self, line):
        # return line.replace("'", '"')
        return line.replace('"', "'")

    def _commit(self, cmd, err="commit error"):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(cmd)
                self.connection.commit()
                return True
            except Exception as ex:
                print(cmd)
                print(red_text("Error:"), err)
                print(ex)
                self.__status = 0
                self.heal()
                return False
            return False

    def _fetchall(self, cmd, err="fetch error"):
         with self.connection.cursor() as cursor:
            try:
                cursor.execute(self._checkQuote(cmd))
                return cursor.fetchall()
            except Exception as ex:
                print(red_text("Error:"), err)
                print(self._checkQuote(cmd))
                print(ex)
                self.__status = 0
                self.heal()
                return {}
            return {}

    def heal(self):
        if self.__status != 1:
            self.connect()
        return self.__status == 1

    def close_connect(self):
        self.connection.close()








# class DatabaseTS(Database):
#     "Database class for TechSupport"
#     def map_table(self):
#         return self._fetchall("select * from map")
        
#     def set_key_text(self, key, text):
#         self._commit(f"insert into map(key_val,text_val) value(\"{key}\",\"{text}\");")

#     def update_text(self, key, text):
#         self._commit(f"update map set text_val = \"{text}\" where key_val = \"{key}\"")
        
#     def delete_text(self, key):
#         self._commit(f"delete from map where key_val =\"{key}\"")

#     def exe_queryKey(self, key):
#         res = self._fetchall(f"select text_val from map where key_val = \"{key}\"")
#         return res[0]['text_val']

#     def is_content(self, key):
#         res = self._fetchall(f"select is_content from pathdir, map where pathdir.id_map = map.id and map.key_val = \"{key}\"")
#         for i in res:
#             if i['is_content'] == True:
#                 return True
#         return False
        
#     def exe_queryPath(self, key):
#         if not self.is_content(key):
#             return None
#         return self._fetchall(f"select dir from pathdir, map where pathdir.id_map = map.id and map.key_val = \"{key}\"")




class SonDB(Database):
    """Database for SON"""
    dblocation = Config.sonDBfiles
    get_access_to_path(dblocation, Config.falcon_username)

    def check_user(self, user_id):
        res = self._fetchall(f"select * from users where user_id = {user_id}")
        return True if len(res) == 1 else False

    def add_user(self, order_key, user_id, user_name=None):
        res = self._fetchall(f"select id from clients where order_key = \"{order_key}\"")
        if len(res) == 1:
            if user_name == None:
                self._commit(f"insert into users(org_id, user_id) value({res[0]['id']}, {user_id})")
            else:
                self._commit(f"insert into users(org_id, user_id, user_name) value({res[0]['id']}, {user_id}, \"{user_name}\")")
            return True
        return False

    def del_user(self, user_id):
        self._commit(f"delete from users where user_id = {user_id}")
                
    def addClient(self, org, order_key):
        if len(self._fetchall(f"select * from clients where org = \"{org}\""))>0:
            self._commit(f"update clients set order_key =\"{order_key}\"")
        else:
            self._commit(f"insert into clients(org, order_key) value(\"{org}\", \"{order_key}\")")

    def addStation(self, serial_id, org_name, mkcb, date, location, description=""):
        org_id = self.getOrgIdByName(org_name) # org_id
        if org_id < 0:
            print("There is no organizations with this name!")
            return
        if len(self._fetchall(f"select * from stations where serial_number = {serial_id}")) == 1:
            print("This station already exist!")
            return
        self._commit(f"insert into stations(serial_number, org_id, mkcb, date_out, location, description_) \
            value({serial_id}, {org_id}, \"{mkcb}\", \"{date}\", \"{location}\", \"{description}\")")

    def addDevice(self, serial_id, station_id, org_name, name, mkcb, date, path, description):
        org_id = self.getOrgIdByName(org_name) # org_id
        if org_id < 0:
            print("There is no organizations with this name!")
            return
        if len(self._fetchall(f"select * from devices where serial_number = {serial_id}")) == 1:
            print("This device already exist!")
            return
        self._commit(f"insert into devices(serial_number, station_number, org_id, device_name, mkcb, date_out, location, description_) \
            value({serial_id}, {station_id}, {org_id},  \"{name}\", \"{mkcb}\", \"{date}\", \"{path}\", \"{description}\")", \
            "insert")

    def getDevices(self, serial_number, client_id):
        res = self._fetchall(f"select * from devices where serial_number = {serial_number}")
        org_id = self._fetchall(f"select org_id from users where user_id ={client_id}")
        if (len(res) == 1) and (len(org_id) == 1):
            if res[0]['org_id'] == int(org_id[0]['org_id']):
                return res[0]
        return {}

    def getStations(self, serial_number, client_id):
        res = self._fetchall(f"select * from stations where serial_number = {serial_number}")
        org_id = self._fetchall(f"select org_id from users where user_id ={client_id}")
        if (len(res) == 1) and (len(org_id) == 1):
            if res[0]['org_id'] == int(org_id[0]['org_id']):
                return res[0]
                # devices = self._fetchall(f"select * from devices where station_number = {res[0]['serial_number']}")
                # return devices
        return {}

    def deleteDevice(self, serial_number, tp="device"):
        self._commit(f"delete from {tp}s where serial_number = {serial_number}", "delete <serial_number> error")

    def delStation(self, serial_number):
        deleteDevice(serial_number, "station")

    def getOrgIdByName(self, name):
        res = self._fetchall(f"select id from clients where org = \"{name}\"")
        # print("org_id = ", res)
        if len(res) == 1:
            return res[0]['id']
        else:
            return -1

    def test(self, serial_number, client_id):
        print(" For serial_number ", serial_number, "and client_id ", client_id)
        stations = self._fetchall(f"select * from stations where serial_number = {serial_number}")
        devices = self._fetchall(f"select * from devices where serial_number = {serial_number}")
        org_id = self._fetchall(f"select org_id from users where user_id ={client_id}")
        print()
        print(stations)
        print()
        print(devices)
        print()
        print(org_id)
        



class TSDB(Database):
    dblocation = Config.tsDBfiles
    get_access_to_path(dblocation, Config.falcon_username)

    def init(self):
        self.main_menu_id = 0


    def getSubMenu(self, parent_id = -1):
        if parent_id < 0:
            parent_id = self.set_main_menu_id()
        menu_items = self._fetchall(f"select * from titles where parent_id = {parent_id}", f"getSubMenu({parent_id})")
        if len(menu_items):
            titles_reply = []
            titles_inline = []
            for elem in menu_items:
                if elem['title_type'] == 1: # Reply
                    titles_reply.append(elem['title'])
                elif elem['title_type'] == 2: # Inline
                    titles_inline.append(elem['title'])
            if titles_reply:
                # print("titles_reply")
                if parent_id > self.main_menu_id:
                    titles_reply.append("Назад")
                return buttonway(titles_reply, "Reply")
            if titles_inline:
                if parent_id > self.main_menu_id:
                    # print("titles_inline")
                    titles_inline.append("Назад")
                return buttonway(titles_inline, "Inline")

    def getContent(self, parent_id = -1):
        if parent_id < 0:
            parent_id = self.main_menu_id
        res = self._fetchall(f"select parent_id, content_text, location from contents where parent_id = {parent_id}", f"getContent{parent_id}")
        if len(res) > 0:
            return res[0]
        else:
            return {}

    def getTitle(self, id):
        res = self._fetchall(f"select * from titles where id = {id}", f"getTitle({id})")
        return res[0]

    def getTitlesByParentId(self, id):
        return self._fetchall(f"select * from titles where parent_id = {id}")

    def getIdByTitle(self, text):
        res = self._fetchall(f"select id from titles where title = \'{text}\'", f"getIdByTitle(\"{text}\")")
        print("have RES")
        print(res)
        if(len(res) > 0):
            return res[0]['id']
        else:
            return -1

    def getIdByCommand(self, text):
        res = self._fetchall(f"select id from titles where command = \"{text}\"", f"getIdByCommand(\"{text}\")")
        if len(res) > 0:
            return res[0]['id']
        else:
            return -1

    def getParentId(self, id):
        res = self._fetchall(f"select parent_id from titles where id = {id}", f"getParentId({id})")
        return res[0]['parent_id']

    def addTitle(self, parent_id, title, title_type, command = None):
        if command != None and self.getIdByCommand(command):
            return "There is the same command."
        mid = self._fetchall(f"select parent_id from titles where title = \"{title}\"", f"addTitle(), mid")
        if len(mid):
            r = self.getSubMenu(mid[0]['parent_id'])
            for i in r:
                if i['title'] == title:
                    return "There is the same title."
        if command:
            self._commit(f"insert into titles(parent_id, title, command, title_type) \
                values({parent_id}, \"{title}\", \"{command}\", {title_type} )")
        else:
            self._commit(f"insert into titles(parent_id, title, title_type) \
                values({parent_id}, \"{title}\", {title_type} )")
        return "Done!"

    def addContent(self, parent_id, content, location = None):
        if len(self.getContent(parent_id)) > 0:
            return f"Already exist with the same id({parent_id})"
        if location:
            self._commit(f"insert into contents(parent_id, content_text, location) \
                values({parent_id}, \"{content}\", \"{self._checkSlash(location)}\" )", "addContent3")
        else:
            self._commit(f"insert into contents(parent_id, content_text) \
                values({parent_id}, \"{content}\" )", "addContent2")
        return "Done!"

    def setTitleCommand(self, id, command):
        if self.getTitle(id):
            self._commit(f"update titles set command = \"{command}\" where id = \"{id}\" ")

    def deleteTitle(self, id):
        self._commit(f"delete from titles where id = {id}")

    def deleteTitleCommand(self, id):
        if self.getTitle(id):
            self._commit(f"update titles set command = NULL where id = {id}")

    def deleteContent(self, parent_id):
        self._commit(f"delete from contents where parent_id = {parent_id}")

    def deleteContentById(self, id):
        self._commit(f"delete from contents where id = {id}")

    def setContentText(self, parent_id, text):
        if self.getContent(parent_id):
            self._commit(f"update contents set content_text = \"{self._checkQuote(text)}\" where parent_id = {parent_id} ")

    def setContentLocation(self, parent_id, location):
        if self.getContent(parent_id):
            self._commit(f"update contents set location = \"{self._checkSlash(location)}\" where parent_id = \"{parent_id}\" ")

    def set_main_menu_id(self):
        self.main_menu_id = self.getIdByTitle('0_main')
        if self.main_menu_id < 0:
            self.main_menu_id = 1
        return self.main_menu_id