import telebot
from telebot import types
import webbrowser
import MDataBase
import Config
import os

#test branch gen


DB = MDataBase.Database("localhost", "root", Config.password, Config.bd_name)
DB.connect()

chat_id_Demiurge = Config.Demiurge
chat_id_Shippuden = Config.Shippuden
chat_id_ITGenerator = Config.ITGenerator

bot = telebot.TeleBot(Config.Token)

def buttonway(list, button):
    if button == "Reply":
        markup = types.ReplyKeyboardMarkup()
        i = 0
        while i < len(list):
            btn1 = types.KeyboardButton(list[i])
            if i + 1 < len(list) and list[i + 1] != " ":
                btn2 = types.KeyboardButton(list[i + 1])
                markup.row(btn1, btn2)
            else:
                markup.row(btn1)
            i += 2
    elif button == "Inline":
        markup = types.InlineKeyboardMarkup()
        i = 0
        while i < len(list):
            btn1 = types.InlineKeyboardButton(list[i], callback_data=list[i])
            if i + 1 < len(list) and list[i + 1] != " ":
                btn2 = types.InlineKeyboardButton(list[i + 1], callback_data=list[i])
                markup.row(btn1, btn2)
            else:
                markup.row(btn1)
            i += 2
    return markup

markup_list = (buttonway(["Проблемы с оборудованием КЕДР", " " , "Проблемы с сетью" ,"Проблемы с программами DCSoft"], "Reply") ,
                   buttonway(["УСО", "Пульт бурильщика", "Датчики", "Кабели", "Назад"], "Reply") ,
                   buttonway(["Wifi точки", "Камеры", "Ip адресса", "Ip телефоны и атс", "Назад"], "Reply")  ,
                   buttonway(["DSServer", " ", "DSPlot", "DSDevice", "Назад"], "Reply") )

markup_list_inline = (buttonway(["Ubiquiti", "TP-Link"], "Inline"),
                      buttonway(["Fanvil X4","Fanvil X1", "Yeastar S20", "Yeastar S50"], "Inline"),
                      buttonway(["Кабели датчиков ГТИ","Магистральные Кабели"], "Inline"),
                      buttonway(["УСО Exd PowerLine","УСО Exd WDSL", "УСО Exn WDSL"], "Inline"),
                      buttonway(["ПНД Exd PowerLine","ПНД Exd WDSL", "ПНД Exn WDSL"], "Inline"),
                      buttonway(["ДНК","ДДИ", "ДУП", "РУД", "ДОП-М", "БЗУД", "ДТ"], "Inline"),
                    )

@bot.message_handler(commands=['start'])
def main(message):
    #bot.send_message(message.chat.id, '<b>Привет!</b>', parse_mode='html')

    text = DB.exe_queryKey("Старт")
    bot.send_message(message.chat.id, text, reply_markup=markup_list[0])
    #bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', reply_markup=markup)
    #bot.register_next_step_handler(message, on_click) Срабатывание следующей функции 

@bot.message_handler(commands=['help'])
def help(message):
    text = DB.exe_queryKey("Помощь")
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['photo','video','voice','video_note','document'])
def feedbackSend(message):
    if message.content_type == "photo":
        bot.send_photo(chat_id_Demiurge,message.photo[0].file_id,f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
        bot.send_photo(chat_id_Shippuden,message.photo[0].file_id,f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
    elif message.content_type == "video":
        bot.send_video(chat_id_Demiurge, message.video.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
        bot.send_video(chat_id_Shippuden, message.video.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
    elif message.content_type == "video_note":
        bot.send_video_note(chat_id_Demiurge, message.video_note.file_id)
        bot.send_video_note(chat_id_Shippuden, message.video_note.file_id)
        bot.send_message(chat_id_Demiurge,f"User {message.from_user.username} ID {message.from_user.id}")
        bot.send_message(chat_id_Shippuden,f"User {message.from_user.username} ID {message.from_user.id}")
    elif message.content_type == "voice":
        bot.send_voice(chat_id_Demiurge,message.voice.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}")
        bot.send_voice(chat_id_Shippuden,message.voice.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}")
    elif message.content_type == "document":
        bot.send_document(chat_id_Demiurge, message.document.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
        bot.send_document(chat_id_Shippuden, message.document.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
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
        bot.send_message(chat_id_Demiurge,f"User {message.from_user.username} ID {message.from_user.id}: {message.text}")
        bot.send_message(chat_id_Shippuden, f"User {message.from_user.username} ID {message.from_user.id}: {message.text}")
        bot.send_message(chat_id_ITGenerator, f"User {message.from_user.username} ID {message.from_user.id}: {message.text}")
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

@bot.message_handler(commands=['books'])
def books(message):
    text = DB.exe_queryKey("Материалы")
    dirs = DB.exe_queryPath("Материалы")
    bot.send_message(message.chat.id, text)
    sendMedia(message, dirs, 'ts')

@bot.message_handler(commands=['son'])
def sysonenum(message):
   # text = DB.exe_queryKey("Материалы")
   # dirs = DB.exe_queryPath("Материалы")
   bot.send_message(message.chat.id, "Введите номер датчика")
   bot.register_next_step_handler(message, son)


@bot.message_handler(commands=['table'])
def gettable(message):
    if message.from_user.id == chat_id_Shippuden or message.from_user.id == chat_id_Demiurge\
            or chat_id_ITGenerator:
        table = DB.map_table()
        for row in table:
            bot.send_message(message.chat.id,f"{row['id']}\t {row['key_val']}  \n {row['text_val']}")

@bot.message_handler(commands=['add', 'update', 'delete'])
def add(message):
    if message.from_user.id == chat_id_Shippuden or message.from_user.id == chat_id_Demiurge\
            or chat_id_ITGenerator:
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
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)
    else:
        bot.send_message(callback.message.chat.id, "Этот пункт еще в разработке.")

@bot.message_handler()
def navigation(message):
    if message.text.lower() == 'проблемы с оборудованием кедр' or message.text == '/hardware':
        bot.send_message(message.chat.id, DB.exe_queryKey('Кедр'),reply_markup=markup_list[1])
    elif message.text.lower() == 'кабели' or message.text == '/cables':
        bot.send_message(message.chat.id, f'Пусто', reply_markup=markup_list_inline[2])
    elif message.text.lower() == 'усо' or message.text == '/uso':
        bot.send_message(message.chat.id, f'Пусто', reply_markup=markup_list_inline[3])
    elif message.text.lower() == 'пульт бурильщика' or message.text == '/pnd':
        bot.send_message(message.chat.id, f'Пусто', reply_markup=markup_list_inline[4])
    elif message.text.lower() == 'датчики' or message.text == '/sensors':
        bot.send_message(message.chat.id, f'Пусто', reply_markup=markup_list_inline[5])
    elif message.text.lower() == 'проблемы с сетью' or message.text == '/network':
        bot.send_message(message.chat.id, DB.exe_queryKey('Сеть'), reply_markup=markup_list[2])
    elif message.text.lower() == 'wifi точки' or message.text == '/wifi':
        bot.send_message(message.chat.id, f'Пусто', reply_markup=markup_list_inline[0])
    elif message.text.lower() == 'ip телефоны и атс' or message.text == '/telephones':
        bot.send_message(message.chat.id, f'Пусто', reply_markup=markup_list_inline[1])
    elif message.text.lower() == 'проблемы с программами dcsoft' or message.text == '/software':
        bot.send_message(message.chat.id, DB.exe_queryKey('DCSoft'), reply_markup=markup_list[3])
    elif message.text.lower() == 'назад':
        bot.send_message(message.chat.id, DB.exe_queryKey("Старт"), reply_markup=markup_list[0])

def sendMedia(message, dirs, method):
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

def son(message):
    number = message.text
    dir = "./son"
    check_number = False
    l_dirs = list(os.walk(dir))
    for i in l_dirs:
        if os.path.basename(i[0]) == number:
            check_number = True
            dirs = []
            for j in os.listdir(i[0]):
                dirs.append(f"{i[0]}/{j}")
            sendMedia(message, dirs, 'son')
    if check_number == False:
        if(message.text in {"/cancel", "/back", "Назад"}):
            return
        bot.send_message(message.chat.id, "Неизвестный номер")
        bot.register_next_step_handler(message, son)








bot.polling(none_stop=True)