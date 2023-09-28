import telebot
from telebot import types
import webbrowser
import MDataBase
import Config
import os
from includes import *
import sys


# DB = MDataBase.Database("localhost", "root", Config.password, Config.bd_name)
DB = MDataBase.DatabaseTS("localhost", "root", Config.password, Config.bd_name_ts)

TSDB = MDataBase.TSDB("localhost", "root", Config.password, Config.bd_name_dispatcher_ts)

SN = MDataBase.SonDB("localhost", "root", Config.password, Config.bd_name_dispatcher_son)


# admins
admins = Config.admins
# chat_id_Demiurge = Config.Demiurge
# chat_id_Shippuden = Config.Shippuden
# chat_id_ITGenerator = Config.ITGenerator

# other
chat_id_TheEyee = Config.TheEyee


bot = telebot.TeleBot(Config.Token)


black_list = []
is_sending = []

menu_position = {}
def get_pos(message):
    if message.from_user.id in menu_position:
        return menu_position[message.from_user.id]
    else:
        return 0


max_lives = 1000
live_countdown = max_lives


def start_bot():
    try:
        print(yellow_text(get_time()), "Starting...")
        DB.connect()
        TSDB.connect()
        SN.connect()
        print(yellow_text(get_time()), "Runned.")
        bot.polling(none_stop=True, timeout=100)
    except Exception as e:
        print(yellow_text(get_time()), "Exception raised.")
        print(e)


@bot.message_handler(commands=['drop', 'stop'])
def drop_bot(message):
    if message.from_user.id in admins:
        print(get_time(), f"Bot has dropped by {message.from_user.id}({message.from_user.username})")
        live_countdown = 0
        bot.stop_polling()
        bot.stop_bot()
        os._exit(0)

@bot.message_handler(commands=['reborn'])
def reset_live_countdown(message):
    if message.from_user.id in admins:
        live_countdown = max_lives

@bot.message_handler(commands=['status'])
def get_drop_status(message):
    print("status")
    if message.from_user.id in admins:
        text = f"live_countdown: <{live_countdown}>"
        print(text)
        bot.send_message(message.chat.id, text, reply_markup=TSDB.getSubMenu(get_pos(message)))


@bot.message_handler(commands=['start'])
def main(message):
    #bot.send_message(message.chat.id, '<b>Привет!</b>', parse_mode='html')

    text = start_text
    bot.send_message(message.chat.id, text, reply_markup=TSDB.getSubMenu(0))
    #bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', reply_markup=markup)
    #bot.register_next_step_handler(message, on_click) Срабатывание следующей функции 

@bot.message_handler(commands=['help'])
def help(message):
    text = DB.exe_queryKey("Помощь")
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['photo','video','voice','video_note','document'])
def feedbackSend(message):
    if message.content_type == "photo":
        for admin_chat in admins:
            bot.send_photo(admin_chat, message.photo[0].file_id,f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
        # bot.send_photo(chat_id_Demiurge, message.photo[0].file_id,f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
        # bot.send_photo(chat_id_Shippuden,message.photo[0].file_id,f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
    elif message.content_type == "video":
        for admin_chat in admins:
            bot.send_video(admin_chat, message.video.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
        # bot.send_video(chat_id_Demiurge, message.video.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
        # bot.send_video(chat_id_Shippuden, message.video.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
    elif message.content_type == "video_note":
        for admin_chat in admins:
            bot.send_video_note(admin_chat, message.video_note.file_id)
            bot.send_message(admin_chat,f"User {message.from_user.username} ID {message.from_user.id}")
        # bot.send_video_note(chat_id_Demiurge, message.video_note.file_id)
        # bot.send_video_note(chat_id_Shippuden, message.video_note.file_id)
        # bot.send_message(chat_id_Demiurge,f"User {message.from_user.username} ID {message.from_user.id}")
        # bot.send_message(chat_id_Shippuden,f"User {message.from_user.username} ID {message.from_user.id}")
    elif message.content_type == "voice":
        for admin_chat in admins:
            bot.send_voice(admin_chat, message.voice.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}")
        # bot.send_voice(chat_id_Demiurge,message.voice.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}")
        # bot.send_voice(chat_id_Shippuden,message.voice.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}")
    elif message.content_type == "document":
        for admin_chat in admins:
            bot.send_document(admin_chat, message.document.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
        # bot.send_document(chat_id_Demiurge, message.document.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
        # bot.send_document(chat_id_Shippuden, message.document.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
    #bot.send_message(chat_id_Demiurge, message)

@bot.message_handler(commands=['mail'])
def feedback(message):
    text = DB.exe_queryKey("Сообщить о проблеме")
    bot.send_message(message.chat.id, text, reply_markup=back_button)
    bot.register_next_step_handler(message, feedbackSendtext)

@bot.message_handler(commands=['feedback'])
def feedback(message):
    text = DB.exe_queryKey("Обратная связь")
    bot.send_message(message.chat.id, text, reply_markup=back_button)
    bot.register_next_step_handler(message, feedbackSendtext)

def feedbackSendtext(message):
    if message.content_type == "text":
        if message.text.lower() in return_keys:
            bot.send_message(message.chat.id, "Действие отменено!", reply_markup=TSDB.getSubMenu(0))
            return
        if message.from_user.id in black_list:
            bot.send_message(message.chat.id, "Действие отклонено!", reply_markup=TSDB.getSubMenu(0))
            return
        text = f"User {message.from_user.username} ID {message.from_user.id}: {message.text}"
        for i in admins:
            bot.send_message(i, text)
        bot.send_message(chat_id_TheEyee, text)
        bot.send_message(message.chat.id, "Сообщение принято в обработку!", reply_markup=TSDB.getSubMenu(0))

    #bot.send_message(chat_id_Demiurge, message)

@bot.message_handler(commands=['site', 'website'])
def site(message):
    #bot.send_message(chat_id_Demiurge, message)
    webbrowser.open('https://gfm.ru/')

@bot.message_handler(commands=['network', 'wifi', 'telephones',
                               'hardware','cables',
                               'software'])
def net(message):
    navigation(message)


is_books = []
@bot.message_handler(commands=['books'])
def books(message):
    if message.from_user.id in is_books:
        return
    is_books.append(message.from_user.id)
    text = DB.exe_queryKey("Материалы")
    dirs = DB.exe_queryPath("Материалы")
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, "Загрузка файлов...")
    sendMedia(message, dirs, 'ts')
    bot.send_message(message.chat.id, "Загрузка завершена.")
    is_books.remove(message.from_user.id)

@bot.message_handler(commands=['son'])
def sysonenum(message):
    if message.text == "Назад":
        bot.send_message(message.chat.id, start_text, reply_markup=TSDB.getSubMenu(0))
    idson = TSDB.getIdByTitle(message.text)
    if idson < 0:
        idson = TSDB.getIdByCommand(message.text)
    res = TSDB.getSubMenu(idson)
    if SN.check_user(message.from_user.id) == False:
        # back_button = telebot.types.ReplyKeyboardMarkup(True)
        # btn1 = types.KeyboardButton("Назад")
        # back_button.row(btn1)
        bot.send_message(message.chat.id, "Введите код доступа (номер договора)", reply_markup=back_button)
        bot.register_next_step_handler(message, adduser, idson)
        return

    bot.send_message(message.chat.id, "Введите номер датчика", reply_markup=res)
    bot.register_next_step_handler(message, son, idson)


def adduser(message, menu_id):
    if SN.add_user(message.text, message.from_user.id, message.from_user.username) == False:
        bot.send_message(message.chat.id, "Отказ!", reply_markup=TSDB.getSubMenu(0))
        bot.register_next_step_handler(message, navigation)
        return
    else:
        bot.send_message(message.chat.id, "Введите номер датчика", reply_markup=TSDB.getSubMenu(menu_id))
        bot.register_next_step_handler(message, son, menu_id)


@bot.message_handler(commands=['table'])
def gettable(message):
    if message.from_user.id in admins:
        table = DB.map_table()
        for row in table:
            bot.send_message(message.chat.id,f"{row['id']}\t {row['key_val']}  \n {row['text_val']}")

@bot.message_handler(commands=['add', 'update', 'delete'])
def add(message):
    if message.from_user.id in admins:
        if message.text == "/update":
            bot.send_message(message.chat.id,"Введи ключ который у тебя уже есть для изменения соблюдая регистр и пробелы ")
        elif message.text == "/delete":
            bot.send_message(message.chat.id, "Введи ключ который ты хочешь удалить соблюдая регистр и пробелы ")
        elif message.text == "/add":
            bot.send_message(message.chat.id, "Первым сообщением введи ключ. Ключи не должны повторятся!!! До 100 символов.")
        bot.send_message(message.chat.id, "Введите назад или отмена для отмены действия ")
        bot.register_next_step_handler(message, addkey, message.text)

def addkey(message, *args):
    if(message.text.lower() == 'назад' or message.text.lower() == 'отмена'):
        bot.send_message(message.chat.id, "Действие отменено")
    else:
        method = args[0]
        key = message.text
        if method != '/delete':
            bot.send_message(message.chat.id, "Теперь можешь вводи текст до 3000 символов. \\n это символ для переноса строки")
        bot.register_next_step_handler(message, addtext, key, method)

def addtext(message, *args):
    text = message.text
    if args[1] == "/add":
        DB.set_key_text(args[0], text)
    elif args[1] == "/delete":
        DB.delete_text(args[0])
    elif args[1] == "/update":
        DB.update_text(args[0], text)

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
    print("map")
    text = getStrMap(0)
    text += "\
        \r\n\
    /help\r\n\
        ...\r\n\
        /books - Обучающие материалы \r\n\
        /mail - Сообщить о проблеме \r\n\
        /feedback - сообщение об ошибке или предложение по улучшению\r\n\
    "
    bot.send_message(message.chat.id, text, reply_markup=TSDB.getSubMenu(get_pos(message)))

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # buttons in messages here
    print(yellow_text(get_time()), f"{callback.message.chat.id}({callback.message.from_user.username}): '{callback.message.text}'")
    if callback.message:
        for row in callback.message.json['reply_markup']['inline_keyboard']:
            if callback.data==row[0]['callback_data']:
                for i in row:
                    print("-", i['text'])
                print(f'Текст на нажатой кнопке: {row[0]["text"]}')
    if callback.data == 'Назад':
        bot.send_message(callback.message.chat.id, start_text, reply_markup=TSDB.getSubMenu(0))
    elif callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, DB.exe_queryKey(callback.data))
        sendMedia(callback.message, DB.exe_queryPath(callback.data), 'ts')




@bot.message_handler()
def navigation(message, menu_id=0):
    if len(message.text) > 100:
        bot.send_message(message.chat.id, "Слишком длинное сообщение!")
        return
    print(yellow_text(get_time()), f"{message.chat.id}({red_text(message.from_user.username)}): '{message.text}'")
    text = "シ"
    location = ""
    if message.text.lower() == 'назад':
        if message.from_user.id in menu_position:
            menu_id = TSDB.getParentId(menu_position[message.from_user.id])
        else:
            menu_id = 0
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
        bot.send_message(message.chat.id, text)
        if location:
            sendFrom(message, location, False)
        menu_position[message.from_user.id] = menu_id
        sysonenum(message)
        return
    menu_position[message.from_user.id] = menu_id
    bot.send_message(message.chat.id, text, reply_markup=TSDB.getSubMenu(menu_id))
    if location:
        sendFrom(message, location, False)



def son(message, menu_id=0, overcount=0):
    number = message.text
    client_id = message.from_user.id
    # SN.test(number, client_id)
    if(message.text in return_keys) or (overcount > 5):
        if(overcount > 5):
            bot.send_message(message.chat.id, "Слишком большое количество ошибок.")
        menu_position[message.from_user.id] = 0
        bot.send_message(message.chat.id, start_text, reply_markup=TSDB.getSubMenu(0))
        bot.register_next_step_handler(message, navigation)
        return
    elif message.text.lower() == "log out":
        SN.del_user(client_id)
        menu_position[message.from_user.id] = 0
        bot.send_message(message.chat.id, start_text, reply_markup=TSDB.getSubMenu(0))
        bot.register_next_step_handler(message, navigation)
        return
    device = SN.getDevices(number, client_id)
    station = SN.getStations(number, client_id)
    if(len(station) == 0 and len(device) == 0):
        bot.send_message(message.chat.id, "Неизвестный номер. Введите корректный номер.", reply_markup=TSDB.getSubMenu(menu_id))
        bot.register_next_step_handler(message, son, menu_id, overcount + 1)
        return
    overcount = 0
    if(len(device) > 0):
        # sendMedia(message, device['location'], 'son')
        loc = device['location']
        if loc[:1] == '.':
            loc = SN.dblocation + loc[1:]
        sendFrom(message, loc, reply_markup=TSDB.getSubMenu(menu_id))

    if(len(station) > 0):
        loc = station['location']
        if loc[:1] == '.':
            loc = SN.dblocation + loc[1:]
        sendFrom(message, loc, False, reply_markup=TSDB.getSubMenu(menu_id))
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

def sendFrom(message, location, subfolders=True, reply_markup=None):
    if message.from_user.id in is_sending:
        bot.send_message(message.chat.id, "Подождите пока загрузятся все файлы.")
    is_sending.append(message.chat.id)
    bot.send_message(message.chat.id, "Загрузка файлов...")
    try:
        sendFromFolder(message, location, subfolders)
    except Exception as e:
        print("Загрузка прервана!")
        print(e)
    if reply_markup == None:
        bot.send_message(message.chat.id, "Загрузка завершена.")
    else:
        bot.send_message(message.chat.id, "Загрузка завершена.", reply_markup)
    is_sending.remove(message.chat.id)

def sendFromFolder(message, location, subfolders=True):
    full_path = os.path.abspath(location)
    l_dirs = os.listdir(full_path)
    for i in l_dirs:
        if os.path.isdir(full_path + "\\" + i):
            if subfolders:
                sendFromFolder(message, full_path + "\\" + i)
        else:
            media = []
            file_type = os.path.splitext(i)
            if file_type[-1] in document_type:
                media.append(types.InputMediaDocument(open(full_path + "\\" + i, 'rb')))
                print("Send: ", full_path + "\\" + i)
            elif file_type[-1] in image_type:
                media.append(types.InputMediaPhoto(open(full_path + "\\" + i, 'rb')))
                print("Send: ", full_path + "\\" + i)
            elif file_type[-1] in video_type:
                media.append(types.InputMediaVideo(open(full_path + "\\" + i, 'rb')))
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




while True:
    print(f"<<<{live_countdown}>>>")
    start_bot()
    if live_countdown < 1:
        break
    live_countdown -= 1

print(yellow_text(get_time()), "END")