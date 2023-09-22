import telebot
from telebot import types
import webbrowser
import MDataBase
import Config
import os


# from includes import *

# DB = MDataBase.Database("localhost", "root", Config.password, Config.bd_name)
DB = MDataBase.DatabaseTS("localhost", "root", Config.password, Config.bd_name_ts)
DB.connect()

TSDB = MDataBase.TSDB("localhost", "root", Config.password, Config.bd_name_dispatcher_ts)
TSDB.connect()

SN = MDataBase.SonDB("localhost", "root", Config.password, Config.bd_name_dispatcher_son)
SN.connect()

# admins
admins = Config.admins
# chat_id_Demiurge = Config.Demiurge
# chat_id_Shippuden = Config.Shippuden
# chat_id_ITGenerator = Config.ITGenerator

# other
chat_id_TheEyee = Config.TheEyee

document_type = {".pdf", ".txt", ".bin", ".doc", ""}
image_type = {".img", ".png", ".bmp"}
video_type = {".mp4"}
audio_type = {".mp3"}


start_text = "Добро пожаловать в бот технической поддержки ГеоФизМаш. Он предназначен для нахождения быстрых ответов, на самые распространённые проблемы. Для полного списка комманд введите /help"

bot = telebot.TeleBot(Config.Token)



is_sending = []

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
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, feedbackSendtext)

@bot.message_handler(commands=['feedback'])
def feedback(message):
    text = DB.exe_queryKey("Обратная связь")
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, feedbackSendtext)

def feedbackSendtext(message):
    if message.content_type == "text":
        text = f"User {message.from_user.username} ID {message.from_user.id}: {message.text}"
        for i in admins:
            bot.send_message(i, text)
        bot.send_message(chat_id_TheEyee, text)

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
        back_button = telebot.types.ReplyKeyboardMarkup(True)
        btn1 = types.KeyboardButton("Назад")
        back_button.row(btn1)
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

@bot.message_handler(commands=['map'])
def project_map(message, *args):
    print("map")
    text = "\
    Проблемы с оборудованием КЕДР (/hardware)\r\n\
        УСО (/uso)\r\n\
            УСО Exd PowerLine (hole)\r\n\
            УСО Exd WDSL (hole)\r\n\
            УСО Exn WDSL (hole)\r\n\
        Пульт бурильщика (/pnd)\r\n\
            ПНД Exd PowerLine (hole)\r\n\
            ПНД Exd WDSL (hole)\r\n\
            ПНД Exn WDSL (hole)\r\n\
        Датчики (/sensors)\r\n\
            ДНК (hole)\r\n\
            ДДИ (hole)\r\n\
            ДУП (hole)\r\n\
            РУД (hole)\r\n\
            ДОП-М (hole)\r\n\
            БЗУД (hole)\r\n\
            ДТ (hole)\r\n\
        Кабели (/cables)\r\n\
            Кабели датчиков ГТИ (hole)\r\n\
            Магистральные Кабели (hole)\r\n\
    Проблемы с сетью (/network)\r\n\
        Wifi точки (/wifi)\r\n\
            Ubiquiti (hole)\r\n\
            TP-Link (hole)\r\n\
        Камеры (/camers) (hole)\r\n\
        Ip адресса (/ip) (hole)\r\n\
        Ip телефоны и атс (/telephones)\r\n\
            Fanvil X1 (hole)\r\n\
            Fanvil X4 (hole)\r\n\
            Yeastar S20 (hole)\r\n\
            Yeastar S50 (hole)\r\n\
    Проблемы с программами DCSoft (/software)\r\n\
        DSServer (/DSServer) (hole)\r\n\
        DSPlot (/DSPlot) (hole)\r\n\
        DSDevice (/DSDevice) (hole)\r\n\
        \r\n\
    /help\r\n\
        ...\r\n\
        /books - Обучающие материалы \r\n\
        /mail - Сообщить о проблеме \r\n\
        /feedback - сообщение об ошибке или предложение по улучшению\r\n\
        /son - Система одного номера\r\n\
    "
    bot.send_message(message.chat.id, text)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # buttons in messages here
    print(f"{callback.message.chat.id}({callback.message.from_user.username}): '{callback.message.text}'")
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
    print(f"{message.chat.id}({message.from_user.username}): '{message.text}'")
    text = "シ"
    if message.text.lower() == 'назад':
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
        if content['location'] != "" and content['location'] != None:
            print(content['location'])
            sendFromFolder(message, content['location'], False)
    if message.text.lower() == "система одного номера":
        menu_id = TSDB.getIdByTitle(message.text)
        bot.send_message(message.chat.id, text)
        sysonenum(message)
        return
    bot.send_message(message.chat.id, text, reply_markup=TSDB.getSubMenu(menu_id))
    # if message.text.lower() == 'проблемы с оборудованием кедр' or message.text == '/hardware':
    #     bot.send_message(message.chat.id, DB.exe_queryKey('Кедр'),reply_markup=markup_list[1])
    # elif message.text.lower() == 'кабели' or message.text == '/cables':
    #     bot.send_message(message.chat.id, f'Пусто', reply_markup=markup_list_inline[2])
    # elif message.text.lower() == 'усо' or message.text == '/uso':
    #     bot.send_message(message.chat.id, f'Пусто', reply_markup=markup_list_inline[3])
    # elif message.text.lower() == 'пульт бурильщика' or message.text == '/pnd':
    #     bot.send_message(message.chat.id, f'Пусто', reply_markup=markup_list_inline[4])
    # elif message.text.lower() == 'датчики' or message.text == '/sensors':
    #     bot.send_message(message.chat.id, f'Пусто', reply_markup=markup_list_inline[5])
    # elif message.text.lower() == 'проблемы с сетью' or message.text == '/network':
    #     bot.send_message(message.chat.id, DB.exe_queryKey('Сеть'), reply_markup=markup_list[2])
    # elif message.text.lower() == 'wifi точки' or message.text == '/wifi':
    #     bot.send_message(message.chat.id, f'Пусто', reply_markup=markup_list_inline[0])
    # elif message.text.lower() == 'ip телефоны и атс' or message.text == '/telephones':
    #     bot.send_message(message.chat.id, f'Пусто', reply_markup=markup_list_inline[1])
    # elif message.text.lower() == 'проблемы с программами dcsoft' or message.text == '/software':
    #     bot.send_message(message.chat.id, DB.exe_queryKey('DCSoft'), reply_markup=markup_list[3])
    # elif message.text.lower() == "система одного номера":
    #     sysonenum(message)
    # elif message.text.lower() == 'назад':
    #     bot.send_message(message.chat.id, DB.exe_queryKey("Старт"), reply_markup=markup_list[0])


def son(message, menu_id=0, overcount=0):
    print("son")
    number = message.text
    client_id = message.from_user.id
    # SN.test(number, client_id)
    if(message.text in {"/cancel", "/back", "Назад"}) or (overcount > 5):
        if(overcount > 5):
            bot.send_message(message.chat.id, "Слишком большое количество ошибок.")
        bot.send_message(message.chat.id, start_text, reply_markup=TSDB.getSubMenu(0))
        bot.register_next_step_handler(message, navigation)
        return
    elif message.text.lower() == "log out":
        SN.del_user(client_id)
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
    print("--")
    print(len(device))
    print(len(station))
    if(len(device) > 0):
        # sendMedia(message, device['location'], 'son')
        loc = device['location']
        if loc[:1] == '.':
            loc = SN.dblocation + loc[1:]
        bot.send_message(message.chat.id, "Загрузка файлов...", reply_markup=TSDB.getSubMenu(menu_id))
        sendFromFolder(message, loc)

    if(len(station) > 0):
        loc = station['location']
        if loc[:1] == '.':
            loc = SN.dblocation + loc[1:]
        bot.send_message(message.chat.id, "Загрузка файлов...", reply_markup=TSDB.getSubMenu(menu_id))
        sendFromFolder(message, loc, False)
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
    bot.send_message(message.chat.id, "Загрузка завершена.")
    is_sending.remove(message.from_user.id)

def sendFromFolder(message, location, subfolders=True):
    if message.from_user.id in is_sending:
        return
    is_sending.append(message.from_user.id)
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
    bot.send_message(message.chat.id, "Загрузка завершена.")
    is_sending.remove(message.from_user.id)




bot.polling(none_stop=True, timeout=100)