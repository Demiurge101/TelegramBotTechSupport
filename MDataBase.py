import Config
from includes import *
import pymysql
from uuid import uuid4
from datetime import datetime
from shutil import copy

from son import SonController

class Database:
    "Base class for Database"
    host = "localhost"
    user = "root"

    def __init__(self, host, user, password, db_name):
        self.host = host
        self.__port = 3306
        self.user = user
        self.password = password
        self.db_name = db_name
        self.__status = 1
        self.__logs = True
        self.__stop_errors = False


    def set_time_out(self, tm=28800):
        self._commit(f"SET GLOBAL connect_timeout={tm}")
        self._commit(f"SET GLOBAL interactive_timeout={tm}")
        self._commit(f"SET GLOBAL wait_timeout={tm}")

    def __del__(self):
        self.close_connect()

    def set_logs(self, log=True):
        self.__logs = log

    def set_stop_errors(self, stop_err=False):
        self.__stop_errors = stop_err

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.__port,
                user=self.user,
                password=self.password,
                database=self.db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            self.__status = 1
            if self.__logs:
                print(f"success {self.db_name}")
        except Exception as ex:
            if self.__logs:
                print(f"Connection refused {self.db_name}")
                print(ex)
                if self.__stop_errors:
                    input("Press enter to continue...")


    def _checkSlash(self, line):
        return line.replace('\\', '\\\\')

    def _checkQuote(self, line):
        # return line.replace("'", '"')
        return line.replace('"', "'")

    def _commit(self, cmd, err="commit error"):
        with self.connection.cursor() as cursor:
            try:
                if self.__logs:
                    print(f"_commit({cmd})")
                cursor.execute(cmd)
                self.connection.commit()
                return True
            except Exception as ex:
                if self.__logs:
                    print(cmd)
                    print(red_text("Error:"), err)
                    print(ex)
                    if self.__stop_errors:
                        input("Press enter to continue...")
                self.__status = 0
                self.heal()
                return False
            return False

    def _fetchall(self, cmd, err="fetch error"):
         with self.connection.cursor() as cursor:
            try:
                if self.__logs:
                    print(f"_fetchall({cmd})")
                cursor.execute(cmd)
                return cursor.fetchall()
            except Exception as ex:
                if self.__logs:
                    print(red_text("Error:"), err)
                    print(cmd)
                    print(ex)
                    if self.__stop_errors:
                        input("Press enter to continue...")
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


    def get_current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]








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
    get_access_to_path(dblocation)
    common_location = Config.uuid_files_location


    def add_file_from_location(self, parent_number, typef, location, name, author='Unknown by SonDB class', rewrite=True):
        # print(green_text(f"add file:  {location}  {name}"))
        son_controller = SonController()
        typef = typef.lower()
        if son_controller.getTextByCode(typef) == '-':
            print(red_text("Wrong file type!"))
            return 'err_type'
        file = self.get_files(number=parent_number, typef=typef)
        print(blue_text(f"FILE: {file}"))
        uuid = uuid4()
        if file:
            print(yellow_text(f"Warning! This file exist! ({typef} for {parent_number})"))
            if not rewrite:
                return file[0]['uuid']
            uuid = file[0]['uuid']
            self.delete_file(file[0]['uuid'])
            sleep(0.1)
        date = datetime.now().strftime("%Y-%m-%d")
        # copy(location, common_location)
        shutil.copyfile(f"{location}/{name}", f"{self.common_location}/{uuid}")
        self._commit(f"insert into files(uuid, typef, namef, author, load_date) value (\"{uuid}\", \"{typef.lower()}\", \"{name}\", \"{author}\", \"{date}\")")
        self._commit(f"insert into filebond(snumber, uuid) value (\"{parent_number}\", \"{uuid}\")")
        return uuid

    def add_file_bond(self, parent_number, uuid):
        r = self._fetchall(f"select * from filebond where snumber = \"{parent_number}\" and uuid = \"{uuid}\"")
        if not len(r):
            self._commit(f"insert into filebond(snumber, uuid) value(\"{parent_number}\", \"{uuid}\")")

    def delete_file(self, uuid):
        print(f"delete_file({uuid})")
        if uuid:
            print("Deleting...")
            self._commit(f"delete from files where uuid = \"{uuid}\"")
            self._commit(f"delete from filebond where uuid = \"{uuid}\"")
            os.remove(f"{self.common_location}/{uuid}")


    def set_file_id(self, uuid, file_id):
        self._commit(f"update files set file_id = \"{file_id}\" where uuid = \"{uuid}\"")

    def get_files(self, number, typef=''):
        typef = typef.lower()
        res = []
        filebonds = self._fetchall(f"select * from filebond where snumber = \"{number}\"")
        for filebond in filebonds:
            file = self._fetchall(f"select * from files where uuid = \"{filebond['uuid']}\"")
            # print("file:", file)
            if not typef or file[0]['typef'] == typef:
                res += file
        # print(f"get_files({number}, {typef}) RES: {res}")
        return res

    def get_file_types(self, number):
        res = []
        if number:
            filebonds = self._fetchall(f"select * from filebond where snumber = \"{number}\"")
            for filebond in filebonds:
                file = self._fetchall(f"select * from files where uuid = \"{filebond['uuid']}\"")
                if len(file):
                    res.append(file[0]['typef'])
                # print(f"get_file_types(), FILE: {file}")
        return res

    def delete_filebond(self, id=0):
        self._commit(f"delete from filebond where id = {id}")

    def delete_dub_filebonds(self):
        numbers = {}
        bonds = self._fetchall(f"select * from filebond")
        for bond in bonds:
            if bond['snumber'] in numbers:
                if bond['uuid'] in numbers[bond['snumber']]:
                    self.delete_filebond(bond['id'])
                else:
                    numbers[bond['snumber']].append(bond['uuid'])
            else:
                numbers[bond['snumber']] = []
                numbers[bond['snumber']].append(bond['uuid'])






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
            self._commit(f"update clients set order_key =\"{order_key}\" where org = \"{org}\"")
        else:
            self._commit(f"insert into clients(org, order_key) value(\"{org}\", \"{order_key}\")")



    def getMKCB(self, mkcb):
        res = self._fetchall(f'select * from decimal_numbers where mkcb = "{mkcb}"')
        # print(f"getMKCB() = {res}")
        if len(res):
            return res[0]
        return {}

    def getMKCBLocation(self,mkcb):
        # res = self._fetchall(f'select location from decimal_numbers where mkcb = "{mkcb}"')
        # if len(res):
        #     return res[0]['location']
        return 'uuid'

    def getMKCBName(self, mkcb):
        res = self._fetchall(f'select _name from decimal_numbers where mkcb = "{mkcb}"')
        if len(res):
            return res[0]['_name']
        return ''

    def addMKCB(self, mkcb, name="", location=""):
        print(f'add mkcb')
        if not self.getMKCB(mkcb):
            print('insert')
            self._commit(f'insert into decimal_numbers(mkcb, _name) values ("{mkcb}", "{name}")')
        else:
            print("change")
            # self.setMKCBLocation(mkcb, location)
            self.setMKCBName(mkcb, name)

    def setMKCBName(self, mkcb, name):
        self._commit(f'update decimal_numbers set _name = "{name}" where mkcb = "{mkcb}"')

    def setMKCBLocation(self, mkcb, location):
        print(yellow_text("Warining! This function obsolete!"))
        # self._commit(f'update decimal_numbers set location = "{location}" where mkcb = "{mkcb}"')

    def deleteMKCB(self, mkcb):
        self._commit(f'delete from decimal_numbers where mkcb = "{mkcb}"')
        self._commit(f"delete from filebond where snumber = \"{mkcb}\"")



    def addStation(self, serial_id, org_name, mkcb, date, location='', description=""):
        org_id = self.getOrgIdByName(org_name) # org_id
        if org_id < 0:
            print(f"There is no organizations with this name({org_name})!")
            return
        if len(self._fetchall(f"select * from stations where serial_number = {serial_id}")) == 1:
            print(f"This station({serial_id}) already exist!")
            return
        self._commit(f"insert into stations(serial_number, org_id, mkcb, date_out, description_) \
            value({serial_id}, {org_id}, \"{mkcb}\", \"{date}\", \"{description}\")")

    def addDevice(self, serial_id, station_id, org_name, name, mkcb, date, path="", description=""):
        org_id = self.getOrgIdByName(org_name) # org_id
        if org_id < 0:
            print(f"There is no organizations with this name({org_name})!")
            return
        if len(self._fetchall(f"select * from devices where serial_number = {serial_id}")) == 1:
            print(f"This device ({serial_id}) already exist!")
            return
        if station_id != None:
            self._commit(f"insert into devices(serial_number, station_number, org_id, device_name, mkcb, date_out, description_) \
                value({serial_id}, {station_id}, {org_id},  \"{name}\", \"{mkcb}\", \"{date}\", \"{description}\")", \
                "insert")
        else:

            self._commit(f"insert into devices(serial_number, org_id, device_name, mkcb, date_out, description_) \
                value({serial_id}, {org_id},  \"{name}\", \"{mkcb}\", \"{date}\", \"{description}\")", \
                "insert")

    def getDevices(self, serial_number, client_id):
        res = self._fetchall(f"select * from devices where serial_number = {serial_number}")
        # org_id = self._fetchall(f"select org_id from users where user_id ={client_id}")
        # if (len(res) == 1) and (len(org_id) == 1):
            # if res[0]['org_id'] == int(org_id[0]['org_id']):
                # return res[0]
        if len(res):
            return res[0]
        return {}

    def getStations(self, serial_number, client_id):
        res = self._fetchall(f"select * from stations where serial_number = {serial_number}")
        # org_id = self._fetchall(f"select org_id from users where user_id ={client_id}")
        # if (len(res) == 1) and (len(org_id) == 1):
        #     if res[0]['org_id'] == int(org_id[0]['org_id']):
        #         return res[0]
        if len(res):
            return res[0]

        return {}

    def deleteDevice(self, serial_number, tp="device"):
        self._commit(f"delete from filebond where snumber = \"{serial_number}\"")
        self._commit(f"delete from {tp}s where serial_number = {serial_number}", "delete <serial_number> error")

    def delStation(self, serial_number):
        deleteDevice(serial_number, "station")

    def addOrg(self, name, key):
        self._commit(f"insert into clients(org, order_key) value (\"{name}\", \"{key}\")")

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
    get_access_to_path(dblocation)
    common_location = Config.uuid_files_location

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
        res = self._fetchall(f"select * from titles where title_id = {id}", f"getTitle({id})")
        return res[0]

    def getTitlesByParentId(self, id):
        return self._fetchall(f"select * from titles where parent_id = {id}")

    def checkSlash(self, text):
        # print(f"checkSlach({text})")
        res = ""
        for i in text:
            # print(i)
            if i == '"':
                # print("spy")
                res += "\\\""
            elif i == "'":
                # print("spy")
                res += "\\\'"
            else:
                res += i
        # print("res:", res)
        return res

    def getIdByTitle(self, text):
        text = self.checkSlash(text)
        res = self._fetchall(f"select title_id from titles where title = \'{text}\'", f"getIdByTitle(\'{text}\')")
        print("have RES:")
        print(res)
        if(len(res) > 0):
            return res[0]['title_id']
        else:
            return -1

    def getIdByCommand(self, text):
        text = self.checkSlash(text)
        res = self._fetchall(f"select title_id from titles where command = \'{text}\'", f"getIdByCommand(\'{text}\')")
        if len(res) > 0:
            return res[0]['title_id']
        else:
            return -1

    def getParentId(self, id):
        res = self._fetchall(f"select parent_id from titles where title_id = {id}", f"getParentId({id})")
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
            self._commit(f"update titles set command = \"{command}\" where title_id = \"{id}\" ")

    def deleteTitle(self, id):
        self._commit(f"delete from titles where title_id = {id}")

    def deleteTitleCommand(self, id):
        if self.getTitle(id):
            self._commit(f"update titles set command = NULL where title_id = {id}")

    def deleteContent(self, parent_id):
        self._commit(f"delete from contents where parent_id = {parent_id}")

    def deleteContentById(self, id):
        self._commit(f"delete from contents where title_id = {id}")

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








    def add_file_from_location(self, title_id, location, name, author='Unknown by TSDB class'):
        print(green_text(f"add file:  {location}  {name}"))
        uuid = uuid4()
        date = datetime.now().strftime("%Y-%m-%d")
        # copy(location, common_location)
        shutil.copyfile(f"{location}/{name}", f"{self.common_location}/{uuid}")
        self._commit(f"insert into files(uuid, namef, author, load_date) value (\"{uuid}\", \"{name}\", \"{author}\", \"{date}\")")
        self._commit(f"insert into filebond(title_id, uuid) value (\"{title_id}\", \"{uuid}\")")
        return uuid

    def add_file_bond(self, title_id, uuid):
        self._commit(f"insert into filebond(title_id, uuid) value(\"{title_id}\", \"{uuid}\")")

    def delete_file(self, uuid):
        print(f"delete_file({uuid})")
        if uuid:
            print("Deleting...")
            self._commit(f"delete from files where uuid = \"{uuid}\"")
            self._commit(f"delete from filebond where uuid = \"{uuid}\"")
            os.remove(f"{self.common_location}/{uuid}")


    def set_file_id(self, uuid, file_id):
        self._commit(f"update files set file_id = \"{file_id}\" where uuid = \"{uuid}\"")

    def get_files(self, title_id):
        print(f'get_files({title_id})')
        res = []
        filebonds = self._fetchall(f"select * from filebond where title_id = \"{title_id}\"")
        print("filebonds:", filebonds)
        for filebond in filebonds:
            file = self._fetchall(f"select * from files where uuid = \"{filebond['uuid']}\"")
            print("file:", file)
            res += file
        return res








class statDB(Database):

    def create_user(self, userid, usertag=None, username=None, userlastname=None):
        self._commit(f"insert into users(user_id) value ({userid})")
        self.update_user(userid, usertag, username, userlastname)

    def update_user(self, userid, usertag=None, username=None, userlastname=None):
        self.set_user_tag(userid, usertag)
        self.set_user_name(userid, username)
        self.set_user_last_name(userid, userlastname)

    def set_user_tag(self, userid, usertag=None):
        self._commit(f"update users set nick = \'{usertag}\' where user_id = {userid}")

    def set_user_name(self, userid, name=None):
        self._commit(f"update users set fname = \'{name}\' where user_id = {userid}")

    def set_user_last_name(self, userid, lastname=None):
        self._commit(f"update users set sname = \'{lastname}\' where user_id = {userid}")

    def get_user(self, userid):
        res = self._fetchall(f"select * from users where user_id = {userid}")
        if len(res):
            return res[0]
        return None

    def delete_user(self, userid):
        self._commit(f"delete from requests where user_id = {userid}")
        self._commit(f"delete from users where user_id = {userid}")




    def add_request(self, userid, request, date_time = None):
        if not date_time:
            date_time = self.get_current_time()
        self._commit(f"insert into requests(rdate, request, user_id) value (\'{date_time}\', \'{request}\', {userid})")


    def fromMessage(self, m):
        # print(f"about user: {m.from_user}")
        if not self.get_user(m.from_user.id):
            self.create_user(m.from_user.id, m.from_user.username, m.from_user.first_name, m.from_user.last_name)
        # self.update_user(m.from_user.id, m.from_user.username, m.from_user.first_name, m.from_user.last_name)
        if m.text[0] == '/':
            cm_index = m.text.find(' ')
            if cm_index >= 0:
                self.add_request(m.from_user.id, m.text[:cm_index])
                return
        self.add_request(m.from_user.id, m.text)



    def getUsersInfo(self, detailed=False, from_datetime="", to_datetime=""):
        res = ""
        counter = 0
        filters = self.__datetime_filters(from_datetime, to_datetime)
        users = self._fetchall(f"select * from users")
        for user in users:
            if filters:
                u = self._fetchall(f"select * from requests{filters} and user_id = {user['user_id']}")
                if not len(u):
                    continue
            else:
                u = self._fetchall(f"select * from requests where user_id = {user['user_id']}")
                if not len(u):
                    continue
            counter += 1
            __id = user['user_id']
            __fname = user['fname']
            __lname = user['sname']
            req_info = f"({self.CountRequestsForUser(__id, from_datetime, to_datetime)} requests, {round(self.__percent(self.CountRequestsForUser(__id, from_datetime, to_datetime), self.CountRequests(from_datetime, to_datetime)), 2)}%)"
            if detailed:
                subcounter = 0
                data = {}
                rtext = f"select * from requests{filters}"
                if filters:
                    rtext += " and"
                else:
                    rtext += " where"
                rtext += f" user_id = {__id}"
                for request in self._fetchall(rtext):
                    if not request['request'] in data:
                        data[request['request']] = 1
                    else:
                        data[request['request']] += 1
                for request in data:
                    subcounter += 1
                    req_info += f"\r\n   {subcounter}) {request}: {data[request]}"
            res += f"<b>{counter}.</b> {__id}:  <b>{user['nick']},  {__fname} {__lname}</b>  {req_info}\r\n"
        return res

    def getRequestsInfo(self, from_datetime="", to_datetime=""):
        res = ""
        counter = 0
        data = {}
        count_requests = self.CountRequests(from_datetime=from_datetime, to_datetime=to_datetime)
        filters = self.__datetime_filters(from_datetime, to_datetime)
        for request in self._fetchall(f"select * from requests{filters}"):
            if not request['request'] in data:
                data[request['request']] = 1
            else:
                data[request['request']] += 1
        for request in data:
            counter += 1
            res += f"{counter}) '{request}':  {data[request]}  ({round(self.__percent(data[request], count_requests), 2)}%)\r\n"
        return res

    def CountUsers(self, from_datetime="", to_datetime=""):
        filters = self.__datetime_filters(from_datetime, to_datetime)
        if filters:
            data = set()
            reqs = self._fetchall(f"select * from requests{filters}")
            for req in reqs:
                data.add(req['user_id'])
            return len(data)
        res = self._fetchall(f"select count(*) from users")
        return res[0]['count(*)']

    def CountRequests(self, from_datetime="", to_datetime=""):
        filters = self.__datetime_filters(from_datetime, to_datetime)
        res = self._fetchall(f"select count(*) from requests{filters}")
        print("getSum() = ")
        print(res[0]['count(*)'])
        return res[0]['count(*)']

    def CountRequestsForUser(self, userid, from_datetime="", to_datetime=""):
        filters = self.__datetime_filters(from_datetime, to_datetime, " ")
        res = self._fetchall(f"select count(*) from requests where user_id = {userid}{filters}")
        return res[0]['count(*)']

    def __percent(self, c, a):
        return c * 100 / a

    def __datetime_filters(self, from_datetime="", to_datetime="", filters=""):
        if from_datetime:
            if not filters:
                filters = " where"
            else:
                filters += " and"
            filters += f" rdate >= \'{from_datetime}\'"
        if to_datetime:
            if not filters:
                filters = " where"
            else:
                filters += " and"
            filters += f" rdate <= \'{to_datetime}\'" 
        return filters
















