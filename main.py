import telebot
from telebot import types
import webbrowser
import MDataBase
import Config

DB = MDataBase.Database("localhost", "root", Config.password, Config.bd_name)
DB.connect()

chat_id_Demiurge = Config.demiurge
chat_id_Shippuden = Config.Shippuden

bot = telebot.TeleBot(Config.Token)

def buttonway(list):
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
    return markup


@bot.message_handler(commands=['start'])
def main(message):
    #bot.send_message(message.chat.id, '<b>Привет!</b>', parse_mode='html')
    markup = buttonway(['Проблемы с оборудованием КЕДР', ' ' , 'Проблемы с сетью' ,'Проблемы с программами DCSoft'])
    """
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Общие проблемы монтажа станции'))
    btn1 = types.KeyboardButton('Проблемы с сетью')
    btn2 = types.KeyboardButton('Проблемы с программами DCSoft')
    markup.row(btn1, btn2)
    """
    text = DB.exe_queryKey("Старт")
    bot.send_message(message.chat.id, text, reply_markup=markup)
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
    bot.send_message(chat_id_Demiurge, message)

@bot.message_handler(commands=['site', 'website'])
def site(message):
    bot.send_message(chat_id_Demiurge, message)
    webbrowser.open('https://gfm.ru/')

@bot.message_handler(commands=['table'])
def gettable(message):
    if message.from_user.id == chat_id_Shippuden or message.from_user.id == chat_id_Demiurge:
        table = DB.map_table()
        for row in table:
            bot.send_message(message.chat.id,f"{row['id']}\t {row['key_val']}  \n {row['text_val']}")

@bot.message_handler(commands=['add', 'update', 'delete'])
def add(message):
    if message.from_user.id == chat_id_Shippuden or message.from_user.id == chat_id_Demiurge:
        if message.text == "/update":
            bot.send_message(message.chat.id,"Введи ключ который у тебя уже есть для изменения соблюдая регистр и пробелы ")
        elif message.text == "/delete":
            bot.send_message(message.chat.id, "Введи ключ который ты хочешь удалить соблюдая регистр и пробелы ")
        elif message.text == "/add":
            bot.send_message(message.chat.id, "Первым сообщением введи ключ. Ключи не должны повторятся!!! До 100 символов.")
        bot.register_next_step_handler(message, addkey, message.text)

def addkey(message, *args):
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


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')



bot.polling(none_stop=True)