import telebot
from telebot import types
import webbrowser
from threads import Threads
from process import Process

from includes import *
import MDataBase
import Config
import sys
from son import *
from statistics import Statistics


# DB = MDataBase.Database("localhost", "root", Config.password, Config.bd_name)
# DB = MDataBase.DatabaseTS("localhost", "root", Config.password, Config.bd_name_ts)

print('init...')
TSDB = MDataBase.TSDB(host=Config.db_host, user=Config.db_login, password=Config.db_password, db_name=Config.db_name_dispatcher_ts)
SN = MDataBase.SonDB(host=Config.db_host, user=Config.db_login, password=Config.db_password, db_name=Config.db_name_dispatcher_son)


# admins
admins = Config.admins

# other
chat_id_TheEyee = Config.TheEyee

DB_timeout = 2147483
max_lives = 5000
max_delay_between_errors = 60
delay_between_errors = 1

token = Config.MyToken

files_location = Config.uuid_files_location

prod = False

for i in sys.argv:
    if i == "-prod":
        token = Config.Token
        prod = True
        print('Production')

start_time = datetime.datetime.now()
last_err_time = start_time

print('bot init...')
bot = telebot.TeleBot(token)
print('threads init...')
thr = Threads()
print('son_controller init...')
son_controller = SonController()
stat = Statistics()
son_stat = Statistics()

main_menu_id = -1

black_list = []
is_sending = []

last_err = ""

menu_position = {}
def get_pos(message):
    global menu_position
    if message.from_user.id in menu_position:
        return menu_position[message.from_user.id]
    else:
        return -1



live_countdown = max_lives


def set_main_menu_id():
    global main_menu_id
    TSDB.init()
    main_menu_id = TSDB.set_main_menu_id()
    print(f"Main menu id: {main_menu_id}")


def start_bot():
    try:
        global last_err_time
        print(yellow_text(get_time()), "Starting...")
        last_err_time = datetime.datetime.now()
        # DB.connect()
        # DB.set_time_out(DB_timeout)
        TSDB.connect()
        TSDB.set_time_out(DB_timeout)
        SN.connect()
        SN.set_time_out(DB_timeout)
        set_main_menu_id()
        print(yellow_text(get_time()), "Runned.")
        bot.polling(none_stop=True, timeout=100)
    except Exception as e:
        global last_err
        global delay_between_errors
        global max_delay_between_errors
        print(yellow_text(get_time()), "Exception raised.")
        print(e)
        if str(e).find(last_err) > -1:
            if delay_between_errors < max_delay_between_errors:
                delay_between_errors += 1
        else:
            last_err = str(e)[:int(len(str(e))/3)]
            delay_between_errors = 1


@bot.message_handler(commands=['drop', 'stop'])
def drop_bot(message):
    stat.fromMessage(message)
    stat.save()
    son_stat.save()
    if message.from_user.id == Config.ITGenerator:
        if message.text.lower() in ['yes', 'y'] or not prod:
            print(yellow_text(get_time()), f"Bot has dropped by {message.from_user.id}({green_text(str(message.from_user.username))})")
            live_countdown = 0
            bot.send_message(message.chat.id, "Bot has ruined!")
            bot.stop_polling()
            bot.stop_bot()
            os._exit(0)
        elif message.text.lower() in ['n', 'no']:
            bot.send_message(message.chat.id, TSDB.getContent()['content_text'], parse_mode='HTML', reply_markup=TSDB.getSubMenu())
        else:
            bot.send_message(message.chat.id, "Are you sure?")
            bot.register_next_step_handler(message, drop_bot)

@bot.message_handler(commands=['reborn'])
def reborn(message):
    stat.fromMessage(message)
    stat.save()
    son_stat.save()
    print(yellow_text(get_time()), f"reborn {message.from_user.id} ({green_text(str(message.from_user.username))})")
    if message.from_user.id in admins:
        reset_live_countdown()
        bot.send_message(message.chat.id, "Done!", reply_markup=TSDB.getSubMenu(get_pos(message)))


def reset_live_countdown():
    global live_countdown
    global max_lives
    global is_sending
    # bot = telebot.TeleBot(Config.MyToken)
    # thr = Threads()
    with thr.rlock():
        is_sending = []
        live_countdown = max_lives

@bot.message_handler(commands=['status'])
def get_drop_status(message):
    stat.fromMessage(message)
    print(yellow_text(get_time()), f"STATUS {message.from_user.id} ({green_text(str(message.from_user.username))})")
    if message.from_user.id in admins:
        text = f"live_countdown: <{live_countdown}>\r\nlen(menu_position) - {len(menu_position)}"
        print(text)
        bot.send_message(message.chat.id, text, reply_markup=TSDB.getSubMenu(get_pos(message)))

@bot.message_handler(commands=['reconnect'])
def reconnect_DB(message):
    stat.fromMessage(message)
    print(yellow_text(get_time()), f"reconnect {message.from_user.id} ({green_text(str(message.from_user.username))})")
    if not message.from_user.id in admins:
        return
    # DB.connect()
    # DB.set_time_out(DB_timeout)
    TSDB.connect()
    TSDB.set_time_out(DB_timeout)
    SN.connect()
    SN.set_time_out(DB_timeout)
    set_main_menu_id()
    bot.send_message(message.chat.id, "Done!", reply_markup=TSDB.getSubMenu(get_pos(message)))

@bot.message_handler(commands=['update_ts'])
def update_ts(message):
    stat.fromMessage(message)
    if not message.from_user.id in admins:
        return
    print(yellow_text(get_time()), f"DB TS has updated by {message.from_user.id}({green_text(str(message.from_user.username))})")
    os.system("python.exe build_tree.py")
    reconnect_DB(message)

@bot.message_handler(commands=['update_son'])
def update_son(message):
    stat.fromMessage(message)
    if not message.from_user.id in admins:
        return
    print(yellow_text(get_time()), f"DB SON has updated by {message.from_user.id}({green_text(str(message.from_user.username))})")
    os.system("python.exe build_DB.py")
    reconnect_DB(message)


def info_send(chat_id, data, do='w', output='info_output'):
    if data:
        bot.send_message(chat_id, data, parse_mode='HTML')
        print(data)
        f = open(output, do)
        f.write(data)
        f.close()

@bot.message_handler(commands=['info'])
def info(message):
    global last_err_time
    print(yellow_text(get_time()), f"'{message.text}': {message.from_user.id} ({green_text(str(message.from_user.username))})")
    # thr.show()
    stat.fromMessage(message)
    if message.from_user.id in admins:
        mtext = message.text.lower()
        # message_text = str(message.text).lower()
        info_text = f'Bot started at {start_time.strftime("<b>%Y.%m.%d</b> <i>%A</i> <b>%H:%M:%S</b>")}\r\n'
        info_text += f'Last error time: {last_err_time.strftime("<b>%Y.%m.%d</b> <i>%A</i> <b>%H:%M:%S</b>")}'
        info_send(message.chat.id, info_text, 'w')
        detailed = False
        if mtext.find('detailed') > -1 or mtext.find('detail') > -1 or mtext.find('d') > -1:
            detailed = True
        if mtext.find('son') > -1 or mtext.find('s') > -1:
            info_text = f'\r\nSON stat ({son_stat.getSum()} requests, {son_stat.getCountUsers()} users):\r\n\r\n'
            info_text += son_stat.getUsersInfo(detailed=detailed)
            info_send(message.chat.id, info_text, 'a')
            info_text = son_stat.getRequestsInfo()
            info_send(message.chat.id, info_text, 'a')
        else:
            info_text = f'Menu stat ({stat.getSum()} requests, {stat.getCountUsers()} users):\r\n\r\n'
            info_text += stat.getUsersInfo(detailed=detailed)
            info_send(message.chat.id, info_text, 'a')
            info_text = stat.getRequestsInfo()
            info_send(message.chat.id, info_text, 'a')

        # bot.send_message(message.chat.id, info_text, parse_mode='HTML')


@bot.message_handler(commands=['send'])
def send_message_to_user(message):
    stat.fromMessage(message)
    if message.from_user.id in admins:
        print(message.text)
        mdata = message.text.split()
        # for i in mdata:
        #     print(f"- {i}")
        if len(mdata) >= 3:
            user_id = mdata[1]
            beginid = message.text.find(mdata[2])
            # print(beginid)
            # print(message.text[beginid:])
            try:
                bot.send_message(user_id, message.text[beginid:])
            except Exception as e:
                print(e)


@bot.message_handler(commands=['start'])
def main(message):
    stat.fromMessage(message)
    #bot.send_message(message.chat.id, '<b>Привет!</b>', parse_mode='html')
    bot.send_message(message.chat.id, TSDB.getContent()['content_text'], parse_mode='HTML', reply_markup=TSDB.getSubMenu())

# @bot.message_handler(commands=['help'])
# def help(message):
#     text = DB.exe_queryKey("Помощь")
#     bot.send_message(message.chat.id, text)
#     if message.from_user.id in admins:
#         text = f"For admins:\r\n /status\r\n /reconnect - reconnect DB\r\n /drop - stop bot\r\n\
#  /update_ts - обновить базу данных техподдержки\r\n /update_son - обновить базу данных системы одного номера"
#         bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['photo','video','voice','video_note','document'])
def content_send(message, chat_id):
    caption = f"From user {str(message.from_user.username)} (id: {message.from_user.id})"
    if message.caption:
        caption += f": {message.caption}"
    if message.content_type == "photo":
        bot.send_photo(chat_id, message.photo[0].file_id, caption)
    elif message.content_type == "video":
        bot.send_video(chat_id, message.video.file_id, caption=caption)
    elif message.content_type == "video_note":
        bot.send_video_note(chat_id, message.video_note.file_id)
        bot.send_message(chat_id, caption)
    elif message.content_type == "voice":
        bot.send_voice(chat_id, message.voice.file_id, caption=caption)
    elif message.content_type == "document":
        bot.send_document(chat_id, message.document.file_id, caption=caption)

@bot.message_handler(commands=['mail'])
def mail(message):
    text = "mail"
    stat.fromMessage(message)
    t_id = TSDB.getIdByCommand(message.text)
    if t_id:
        text = TSDB.getContent(t_id)['content_text']
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=back_button)
    bot.register_next_step_handler(message, feedbackHandler)

def mailHandler(message):
    print(message.content_type)
    if message.content_type == "sticker":
        print("sending")
        bot.send_sticker(Config.ITGenerator, message.sticker.file_id)
    bot.send_message(message.chat.id, "Ok!", reply_markup=TSDB.getSubMenu(get_pos(message)))

@bot.message_handler(commands=['feedback'])
def feedback(message):
    text = "feedback"
    stat.fromMessage(message)
    t_id = TSDB.getIdByCommand(message.text)
    if t_id:
        text = TSDB.getContent(t_id)['content_text']
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=back_button)
    bot.register_next_step_handler(message, feedbackHandler)

def feedbackHandler(message):
    if message.from_user.id in black_list:
        bot.send_message(message.chat.id, "Действие отклонено!", reply_markup=TSDB.getSubMenu())
        return
    if message.content_type == "text":
        if message.text.lower() in return_keys:
            bot.send_message(message.chat.id, "Действие отменено!", reply_markup=TSDB.getSubMenu())
            return
        text = f"User {str(message.from_user.username)} ID {message.from_user.id}: {message.text}"
        f = open("feedback.txt", 'w')
        f.write(text)
        f.close()
        for i in admins:
            bot.send_message(i, text)
        bot.send_message(chat_id_TheEyee, text)
        bot.send_message(message.chat.id, "Сообщение принято в обработку!", reply_markup=TSDB.getSubMenu(get_pos(message)))
    else:
        for admin_chat in admins:
            content_send(message, admin_chat)
        # content_send(message, Config.ITGenerator)
        bot.send_message(message.chat.id, "Принято в обработку!", reply_markup=TSDB.getSubMenu(get_pos(message)))
    #bot.send_message(chat_id_Demiurge, message)

    if message.content_type == "sticker":
        bot.send_message(chat_id_TheEyee, f"Вадим тут стицкер как ты хотел from user {str(message.from_user.username)} ID {message.from_user.id}", reply_markup=TSDB.getSubMenu(get_pos(message)))
        # bot.send_message(chat_id_TheEyee, 'стицкер', reply_markup=TSDB.getSubMenu(get_pos(message)))
        bot.send_sticker(chat_id_TheEyee, message.sticker.file_id)

        bot.send_message(Config.ITGenerator, f"From user {str(message.from_user.username)} ID {message.from_user.id}", reply_markup=TSDB.getSubMenu(get_pos(message)))
        bot.send_sticker(Config.ITGenerator, message.sticker.file_id)
        

@bot.message_handler(commands=['site'])
def site(message):
    stat.fromMessage(message)
    #bot.send_message(chat_id_Demiurge, message)
    webbrowser.open('https://gfm.ru/')

# @bot.message_handler(commands=['network', 'wifi', 'telephones',
#                                'hardware','cables',
#                                'software'])
# def net(message):
#     navigation(message)


# is_books = []
# @bot.message_handler(commands=['books'])
# def books(message):
#     if message.from_user.id in is_books:
#         return
#     is_books.append(message.from_user.id)
#     text = DB.exe_queryKey("Материалы")
#     dirs = DB.exe_queryPath("Материалы")
#     bot.send_message(message.chat.id, text)
#     bot.send_message(message.chat.id, "Загрузка файлов...")
#     sendMedia(message, dirs, 'ts')
#     bot.send_message(message.chat.id, "Загрузка завершена.")
#     is_books.remove(message.from_user.id)

@bot.message_handler(commands=['son'])
def sysonenum(message):
    global main_menu_id
    son_stat.fromMessage(message)
    if message.text == "Назад":
        main_menu_id = 1 # 
        bot.send_message(message.chat.id, TSDB.getContent()['content_text'], parse_mode='HTML', reply_markup=TSDB.getSubMenu())
    idson = TSDB.getIdByTitle(message.text)
    if idson < 0:
        idson = TSDB.getIdByCommand(message.text)
    res = TSDB.getSubMenu(idson)
    # print("M:", res)
    if not res:
        res = back_button
    # check login
    # if SN.check_user(message.from_user.id) == False:
    #     bot.send_message(message.chat.id, "Введите код доступа (номер договора)", reply_markup=back_button)
    #     bot.register_next_step_handler(message, adduser, idson)
    #     return

    bot.send_message(message.chat.id, son_text['begin'], parse_mode='HTML', reply_markup=res)
    # thread(bot.register_next_step_handler, (message, son, idson))
    bot.register_next_step_handler(message, son, idson)


def adduser(message, menu_id):
    if SN.add_user(message.text, message.from_user.id, message.from_user.username) == False:
        bot.send_message(message.chat.id, "Отказ!", reply_markup=TSDB.getSubMenu())
        bot.register_next_step_handler(message, navigation)
        return
    else:
        bot.send_message(message.chat.id, son_text['begin'], parse_mode='HTML', reply_markup=TSDB.getSubMenu(menu_id))
        bot.register_next_step_handler(message, son, menu_id)


# @bot.message_handler(commands=['table'])
# def gettable(message):
#     if message.from_user.id in admins:
#         table = DB.map_table()
#         for row in table:
#             bot.send_message(message.chat.id,f"{row['id']}\t {row['key_val']}  \n {row['text_val']}")


def getStrMap(parent_id, pre=""):
    titles = TSDB.getTitlesByParentId(parent_id)
    res = ""
    for title in titles:
        cmd = ""
        if title['command']:
            cmd = f" ({title['command']})"

        row = f"{pre}{title['title']}{cmd}"
        table = getStrMap(title['id'], pre + '   ')
        res += f"{row}\r\n{table}"
    return res

@bot.message_handler(commands=['map'])
def project_map(message, *args):
    stat.fromMessage(message)
    print(yellow_text(get_time()), f"{message.from_user.id}({green_text(str(message.from_user.username))}): '{message.text}'")
    text = getStrMap(0)
    bot.send_message(message.chat.id, text, reply_markup=TSDB.getSubMenu(get_pos(message)))
    if message.from_user.id in admins:
        text = f"""For admins:
        /status
        /reborn
        /reconnect - reconnect DB
        /drop - stop bot
        /update_ts - обновить базу данных техподдержки
        /update_son - обновить базу данных системы одного номера
        /info (|son) (|detailed)
        /send <id> <text>"""
        bot.send_message(message.chat.id, text)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # buttons in messages here
    print(yellow_text(get_time()), f"{callback.message.chat.id}({str(callback.message.from_user.username)}): '{callback.message.text}'")
    if callback.message:
        for row in callback.message.json['reply_markup']['inline_keyboard']:
            if callback.data==row[0]['callback_data']:
                for i in row:
                    print("-", i['text'])
                print(f'Текст на нажатой кнопке: {row[0]["text"]}')
    if callback.data == 'Назад':
        bot.send_message(callback.message.chat.id, TSDB.getContent(), reply_markup=TSDB.getSubMenu())
    elif callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, DB.exe_queryKey(callback.data))
        sendMedia(callback.message, DB.exe_queryPath(callback.data), 'ts')




@bot.message_handler(content_types='text')
def navigation(message, menu_id=0):
    global main_menu_id
    global menu_position
    # print(f"navigation({message.text})")
    if menu_id == 0:
        menu_id = main_menu_id
    if message.text == None:
        print(red_text("message.text == None"))
        return
    if len(message.text) > 100:
        bot.send_message(message.chat.id, "Слишком длинное сообщение!")
        return
    stat.fromMessage(message)
    try:
        print(yellow_text(get_time()), f"{message.from_user.id}({green_text(str(message.from_user.username))}): '{message.text}'")
    except Exception as e:
        print(f"navigation({message.text})")
    text = "シ"
    location = ""
    if message.text.lower() == 'назад':
        print("Back")
        if message.from_user.id in menu_position:
            print("IN")
            print("position: ", menu_position[message.from_user.id])
            menu_id = TSDB.getParentId(menu_position[message.from_user.id])
            if menu_id < main_menu_id:
                menu_id = menu_position[message.from_user.id]
            print("done")
        else:
            print("NOT IN")
            menu_id = main_menu_id
            print("done")
        print("Back.")
    else:
        menu_id = TSDB.getIdByTitle(message.text)
    if menu_id < 0:
        menu_id = TSDB.getIdByCommand(message.text)
        if menu_id < 0:
            return
    content = TSDB.getContent(menu_id)
    if content:
        if content['content_text']:
            # bot.send_message(message.chat.id, content['content_text'])
            text = content['content_text']
            # print(text)
        if content['location'] != "" and content['location'] != None:
            location = content['location']
            print(content['location'])
            # sendFromFolder(message, content['location'], False)
    if message.text.lower() == "система одного номера":
        menu_id = TSDB.getIdByTitle(message.text)
        bot.send_message(message.chat.id, text, parse_mode='HTML')
        if location:
            # thread(sendFrom, (message, location, False))
            thr.run(sendFrom, (message, location, False))
            # sendFrom(message, location, False)
        menu_position[message.from_user.id] = menu_id
        sysonenum(message)
        return
    if len(TSDB.getTitlesByParentId(menu_id)) > 0:
        menu_position[message.from_user.id] = menu_id
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=TSDB.getSubMenu(menu_id))
    if location and message.text.lower() != 'назад':
        # thread(sendFrom, (message, location, False))
        thr.run(sendFrom, (message, location, False))
        # sendFrom(message, location, False)



def son(message, menu_id=0, overcount=0):
    global main_menu_id
    global menu_position
    number = message.text
    client_id = message.from_user.id
    son_stat.fromMessage(message)
    # SN.test(number, client_id)
    # print("Parsed:", son_controller.parse_type(message.text.lower()))
    if(message.text in return_keys) or message.text == '/start' or (overcount > 5):
        if(overcount > 5):
            bot.send_message(message.chat.id, "Слишком большое количество ошибок.")
        menu_position[message.from_user.id] = main_menu_id
        bot.send_message(message.chat.id, TSDB.getContent()['content_text'], parse_mode='HTML', reply_markup=TSDB.getSubMenu())
        # bot.register_next_step_handler(message, navigation)
        son_controller.deleteUser(message.from_user.id)
        son_controller.deleteUserLocation(message.from_user.id)
        return
    elif message.text.lower() == "log out":
        SN.del_user(client_id)
        menu_position[message.from_user.id] = main_menu_id
        bot.send_message(message.chat.id, TSDB.getContent()['content_text'], parse_mode='HTML', reply_markup=TSDB.getSubMenu())
        # bot.register_next_step_handler(message, navigation)
        son_controller.deleteUser(message.from_user.id)
        son_controller.deleteUserLocation(message.from_user.id)
        return
    elif message.text[0] == '/':
        return navigation(message)
    # parsed_type = son_controller.parseType(message.text)
    codes_location = son_controller.getLocation()
    mkcb_location = ''
    parsed_type = son_controller.setNumber(message.from_user.id, message.text)
    # parsed_type = son_controller.getType(message.from_user.id)
    print(f"Parsed: {parsed_type}")
    if parsed_type == 'number':
        device = SN.getDevices(number, client_id)
        station = SN.getStations(number, client_id)
        if(len(station) == 0 and len(device) == 0):
            print("emty mark")
            m = TSDB.getSubMenu(menu_id)
            if not m:
                m = back_button
            bot.send_message(message.chat.id, son_text['wrong_number'], parse_mode='HTML', reply_markup=m)
            bot.register_next_step_handler(message, son, menu_id, overcount + 1)
            return
        overcount = 0
        if(len(device) > 0):
            print('device')
            # sendMedia(message, device['location'], 'son')
            loc = 'uuid'
            # decimal_number = device['mkcb']
            son_controller.setNumber(message.from_user.id, device['mkcb'][5:])
            mkcb_location = 'uuid'
            mkcb_location = SN.getMKCBLocation(device['mkcb'])
            # print(f'mkcb_location d = {mkcb_location}')
            if loc[:1] == '.':
                loc = SN.dblocation + loc[1:]
            # elif loc == 'uuid':
            #     files = SN.get_files(number)
            codes_location = loc
            son_controller.setUserLocation(message.from_user.id, loc)
            if checkFiles(loc, False):
                thr.run(sendFrom, (message, loc, False, TSDB.getSubMenu(menu_id)))
            # sendFrom(message, loc, reply_markup=TSDB.getSubMenu(menu_id))

        if(len(station) > 0):
            print('station')
            loc = 'uuid'
            # decimal_number = station['mkcb']
            son_controller.setNumber(message.from_user.id, station['mkcb'][5:])
            mkcb_location = 'uuid'
            # print(f'mkcb_location s = {mkcb_location}')
            if loc[:1] == '.':
                loc = SN.dblocation + loc[1:]
            # elif loc == 'uuid':
            #     files = SN.get_files(number)
                # loc = f"{files_location}/{loc[4:]}"
            codes_location = loc
            son_controller.setUserLocation(message.from_user.id, loc)
            if checkFiles(loc, False):
                thr.run(sendFrom, (message, loc, False, TSDB.getSubMenu(menu_id)))
            # sendFrom(message, loc, False, reply_markup=TSDB.getSubMenu(menu_id))
    elif parsed_type == 'mkcb':
        son_controller.deleteSerialNumber(message.from_user.id)
        mkcb_location = SN.getMKCBLocation(f'МКЦБ.{son_controller.getDecimalNumber(message.from_user.id)}')

    if parsed_type in ['mkcb', 'number']:
        sub_menu = son_controller.getCodes(message.from_user.id, codes_location, mkcb_location)
        print(sub_menu)
        files_obj = []
        if codes_location == 'uuid':
            files_obj = SN.get_file_types(son_controller.getSerialNumber(message.from_user.id))
            print(f"for {son_controller.getSerialNumber(message.from_user.id)}")
            print(f"get: {files_obj}")
        if mkcb_location == 'uuid':
            files_obj += SN.get_file_types(f'МКЦБ.{son_controller.getDecimalNumber(message.from_user.id)}')
            print(f"for {son_controller.getDecimalNumber(message.from_user.id)}")
            print(f"get: {files_obj}")
        for file_obj in files_obj:
            print(file_obj)
            sub_menu.append(son_controller.getTextByCode(file_obj.lower()))

        # print("sub_menu:", sub_menu)
        res = '-'
        if sub_menu:
            res = f"{son_text['you_can_get_docs']}\r\n\r\n"
            for code in sub_menu:
                res += f"{code}\r\n"
            res += f"\r\n{son_text['enter_code_for_download']}"
        else:
            res = son_text['wrong_number']
        bot.send_message(message.chat.id, res, parse_mode='HTML', reply_markup=back_button)
    elif parsed_type in {'d_code', 'd_icode'}:
        if parsed_type == 'd_icode':
            number = son_controller.inverseCode(message.text)
        if son_controller.getType(message.from_user.id):
            d_number = f'МКЦБ.{son_controller.getDecimalNumber(message.from_user.id)}'
            # print(f'd_number = {d_number}')
            d_name = SN.getMKCBName(d_number)
            d_loc = SN.getMKCBLocation(d_number)
            # need to fix in future (send multiple files, remove uuid column)
            if d_loc == 'uuid':
                files = SN.get_files(d_number, number)
                print("Files:")
                for f in files:
                    # print(f)
                    flct = f"{files_location}/{f['uuid']}"
                    print(f['file_id'])
                    sended = False
                    if f['file_id'] != None:
                        try:
                            print(f"Try send old file (file_id: {f['file_id']})")
                            bot.send_document(message.chat.id, f['file_id'])
                            sended = True
                        except Exception as e:
                            print(e)
                    if not sended:
                        print('Sending new file...')
                        file_id = sendFileByRequest(message.chat.id, f['uuid'], files_location, f['namef'])
                        SN.set_file_id(f['uuid'], file_id)

                    
                    # sendFile(message, f['uuid'], files_location, f['namef'])

            # print(f"d_name = {d_name}")
            # lct = f"{son_controller.getLocation()}/{d_number}/{message.text} {d_number}"

            # lct = f'{d_loc}/{number} {d_number}' # number = message.text
            # if checkFiles(lct):
            #     thr.run(sendFrom, (message, lct, True, back_button, son_text['another_code_or_number']))
            # else:
            #     bot.send_message(message.chat.id, son_text['wrong_code'], parse_mode='HTML', reply_markup = back_button)
        else:
            bot.send_message(message.chat.id, son_text['wrong_number'], parse_mode='HTML', reply_markup = back_button)
    elif parsed_type in {'s_code', 's_icode'}:
        if parsed_type == 's_icode':
            number = son_controller.inverseCode(message.text)
        if son_controller.getUserLocation(message.from_user.id) == 'uuid':
            files = SN.get_files(son_controller.getSerialNumber(message.from_user.id), number)
            print("Files:")
            for f in files:
                flct = f"{files_location}/{f['uuid']}"
                print(f['file_id'])
                sended = False
                if f['file_id'] != None:
                    try:
                        print('old send')
                        bot.send_document(message.chat.id, f['file_id'])
                        sended = True
                    except Exception as e:
                        print(e)
                if not sended:
                    print('new send')
                    file_id = sendFileByRequest(message.chat.id, f['uuid'], files_location, f['namef'])
                    SN.set_file_id(f['uuid'], file_id)


        elif son_controller.getUserLocation(message.from_user.id):
            lct = f"{son_controller.getUserLocation(message.from_user.id)}/{number} {son_controller.getSerialNumber(message.from_user.id)}"
            if checkFiles(lct):
                thr.run(sendFrom, (message, lct, True, back_button, son_text['another_code_or_number']))
            else:
                bot.send_message(message.chat.id, son_text['wrong_code'], parse_mode='HTML', reply_markup = back_button)
                # bot.send_message(message.chat.id, "Нет файлов", reply_markup = back_button)
        else:
            bot.send_message(message.chat.id, son_text['wrong_number'], parse_mode='HTML', reply_markup = back_button)
    else:
        response_text = "unknown"
        if son_controller.getType(message.from_user.id):
            response_text = son_text['wrong_code']
        else:
            response_text = son_text['wrong_number']
        bot.send_message(message.chat.id, response_text, parse_mode='HTML', reply_markup = back_button)
    bot.register_next_step_handler(message, son, menu_id, 0)



def sendMedia(message, dirs, method):
    if message.from_user.id in is_sending:
        return
    is_sending.append(message.from_user.id)
    if dirs is not None:
        files = []
        type_names = []
        if method == 'son':
            for i in dirs:
                type_names.append(os.path.basename(i))
                files.append(os.listdir(i))
            dir = os.path.dirname(dirs[0])
        else:
            for i in dirs:
                type_names.append(os.path.basename(i['dir']))
                files.append(os.listdir(i['dir']))
            dir = os.path.dirname(dirs[0]['dir'])
        media = []
        i = 0
        while i < type_names.__len__():
            if type_names[i] == "document":
                media.clear()
                for j in files[i]:
                    s = f"{dir}/{type_names[i]}/{j}"
                    media.append(types.InputMediaDocument(open(f"{dir}/{type_names[i]}/{j}", 'rb')))
            elif type_names[i] == "photo":
                media.clear()
                for j in files[i]:
                    media.append(types.InputMediaPhoto(open(f"{dir}/{type_names[i]}/{j}", 'rb')))
            elif type_names[i] == "video":
                media.clear()
                for j in files[i]:
                    media.append(types.InputMediaVideo(open(f"{dir}/{type_names[i]}/{j}", 'rb')))
            if len(media) != 0:
                while len(media) > 10:
                    submedia = media[0:10]
                    media = media[10:]
                    bot.send_media_group(message.chat.id, submedia)
                    #bot.send_media_group(message.chat.id, media)
                else:
                    bot.send_media_group(message.chat.id, media)
            i += 1
    # bot.send_message(message.chat.id, "Загрузка завершена.")
    is_sending.remove(message.from_user.id)

def sendFrom(message, location, subfolders=True, reply_markup=None, text='', parse_mode='HTML'):
    with thr.rlock():
        if message.from_user.id in is_sending:
            bot.send_message(message.chat.id, "Подождите пока загрузятся все файлы.")
            return
        is_sending.append(message.chat.id)
    bot.send_message(message.chat.id, "Загрузка файлов...")
    try:
        sendFromFolder(message, location, subfolders)
    except Exception as e:
        # print("Загрузка прервана!")
        bot.send_message(message.chat.id, "Загрузка прервана.")
        if message.from_user.id in admins:
            bot.send_message(message.chat.id, str(e))
        # print(e)
    if reply_markup == None:
        bot.send_message(message.chat.id, "Загрузка завершена.")
    else:
        bot.send_message(message.chat.id, "Загрузка завершена.", reply_markup=reply_markup)
    if text:
        bot.send_message(message.chat.id, text, parse_mode=parse_mode)
    with thr.rlock():
        is_sending.remove(message.chat.id)

def sendFromFolder(message, location, subfolders=True):
    full_path = os.path.abspath(location)
    l_dirs = os.listdir(full_path)
    for i in l_dirs:
        if os.path.isdir(full_path + "/" + i):
            if subfolders:
                sendFromFolder(message, full_path + "/" + i)
        else:
            sendFile(message, i, full_path)
            # media = []
            # file_type = os.path.splitext(i)
            # if file_type[-1] in document_type:
            #     media.append(types.InputMediaDocument(open(full_path + "/" + i, 'rb')))
            #     # print("Send: ", full_path + "/" + i)
            # elif file_type[-1] == '.lnk':
            #     print(f'sending link file: {full_path}/{i}')
            #     sp = getLinkSource(f"{full_path}/{i}")
            #     # print(yellow_text(f"sp<'{sp}'>"))
            #     if sp[0] == '.':
            #         spa = sp[1:]
            #         # print(yellow_text(f'spa<{spa}>'))
            #         for loc in Config.db_locations:
            #             # print(yellow_text(f'loc<{loc}>'))
            #             spr = loc + spa
            #             if os.path.exists(spr):
            #                 # print(green_text('Exist!'))
            #                 sp = spr
            #                 break
            #     if os.path.isdir(sp):
            #         sendFromFolder(message, sp)
            #     else:
            #         print('not directory (lnk)')
            #         media.append(types.InputMediaDocument(open(sp, 'rb')))
            # elif file_type[-1] in image_type:
            #     media.append(types.InputMediaPhoto(open(full_path + "/" + i, 'rb')))
            #     # print("Send: ", full_path + "/" + i)
            # elif file_type[-1] in video_type:
            #     media.append(types.InputMediaVideo(open(full_path + "/" + i, 'rb')))
            # elif file_type[-1] in audio_type:
            #     pass
            # # print("len media = ", len(media))
            # if len(media) != 0:
            #     while len(media) > 10:
            #         submedia = media[0:10]
            #         media = media[10:]
            #         bot.send_media_group(message.chat.id, submedia)
            #         #bot.send_media_group(message.chat.id, media)
            #     else:
            #         bot.send_media_group(message.chat.id, media)

def sendFile(message, name, full_path, fname = None, caption=''):
    media = []
    file_type = os.path.splitext(name)
    if file_type[-1] in document_type:
        media.append(types.InputMediaDocument(open(full_path + "/" + name, 'rb'), caption=caption))
        # print("Send: ", full_path + "/" + name)
    elif file_type[-1] == '.lnk':
        print(f'sending link file: {full_path}/{name}')
        sp = getLinkSource(f"{full_path}/{name}")
        # print(yellow_text(f"sp<'{sp}'>"))
        if sp[0] == '.':
            spa = sp[1:]
            # print(yellow_text(f'spa<{spa}>'))
            for loc in Config.db_locations:
                # print(yellow_text(f'loc<{loc}>'))
                spr = loc + spa
                if os.path.exists(spr):
                    # print(green_text('Exist!'))
                    sp = spr
                    break
        if os.path.isdir(sp):
            sendFromFolder(message, sp)
        else:
            print('not directory (lnk)')
            media.append(types.InputMediaDocument(open(sp, 'rb')))
    elif file_type[-1] in image_type:
        media.append(types.InputMediaPhoto(open(full_path + "/" + name, 'rb')))
        # print("Send: ", full_path + "/" + name)
    elif file_type[-1] in video_type:
        media.append(types.InputMediaVideo(open(full_path + "/" + name, 'rb')))
    elif file_type[-1] in audio_type:
        pass
    # print("len media = ", len(media))
    if len(media) != 0:
        while len(media) > 10:
            submedia = media[0:10]
            media = media[10:]
            bot.send_media_group(message.chat.id, submedia)
            #bot.send_media_group(message.chat.id, media)
        else:
            bot.send_media_group(message.chat.id, media)


def sendFileByRequest(chat_id, fname, flocation, fnewname='document.png'):
    fabsname = f"{flocation}/{fname}"
    document = open(fabsname, "rb")
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    response = requests.post(url, data={'chat_id': chat_id}, files={'document': (fnewname, document)})
    # part below, just to make human readable response for such noobies as I
    content = response.content.decode("utf8")
    js = json.loads(content)
    # print()
    # print(f"js: {js['result']['document']}")

    return js['result']['document']['file_id']
    


while True:
    print()
    print(f"<<<{red_text(str(live_countdown))}>>>")
    start_bot()
    stat.save()
    son_stat.save()
    if live_countdown < 1:
        break
    print(f"Sleep {delay_between_errors}s")
    sleep(delay_between_errors)
    live_countdown -= 1

print(yellow_text(get_time()), "END")