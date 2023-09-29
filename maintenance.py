import telebot
from telebot import types
import webbrowser
import MDataBase
import Config
import os
from includes import *
import sys

from threads import thread

# admins
admins = Config.admins

# other
chat_id_TheEyee = Config.TheEyee


bot = telebot.TeleBot(Config.Token)


@bot.message_handler(commands=['start'])
def main(message):
    #bot.send_message(message.chat.id, '<b>Привет!</b>', parse_mode='html')

    text = start_text
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['photo','video','voice','video_note','document'])
def feedbackSend(message):
    if message.content_type == "photo":
        for admin_chat in admins:
            bot.send_photo(admin_chat, message.photo[0].file_id,f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
    elif message.content_type == "video":
        for admin_chat in admins:
            bot.send_video(admin_chat, message.video.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")
    elif message.content_type == "video_note":
        for admin_chat in admins:
            bot.send_video_note(admin_chat, message.video_note.file_id)
            bot.send_message(admin_chat,f"User {message.from_user.username} ID {message.from_user.id}")
    elif message.content_type == "voice":
        for admin_chat in admins:
            bot.send_voice(admin_chat, message.voice.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}")
    elif message.content_type == "document":
        for admin_chat in admins:
            bot.send_document(admin_chat, message.document.file_id, caption=f"User {message.from_user.username} ID {message.from_user.id}:{message.caption}")



@bot.message_handler(commands=['feedback'])
def feedback(message):
    text = "Введите сообщение, его увидят разработчики:"
    bot.send_message(message.chat.id, text, reply_markup=back_button)
    bot.register_next_step_handler(message, feedbackSendtext)

def feedbackSendtext(message):
    if message.content_type == "text":
        if message.text.lower() in return_keys:
            bot.send_message(message.chat.id, "Действие отменено!")
            return
        if message.from_user.id in black_list:
            bot.send_message(message.chat.id, "Действие отклонено!")
            return
        text = f"User {message.from_user.username} ID {message.from_user.id}: {message.text}"
        for i in admins:
            bot.send_message(i, text)
        bot.send_message(chat_id_TheEyee, text)
        bot.send_message(message.chat.id, "Сообщение принято в обработку!")

    #bot.send_message(chat_id_Demiurge, message)

@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://gfm.ru/')


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # buttons in messages here
    print(yellow_text(get_time()), f"{callback.message.chat.id}({callback.message.from_user.username}): '{callback.message.text}'")




@bot.message_handler()
def navigation(message, menu_id=0):
    bot.send_message(message.chat.id, "Бот в ремонте!", reply_markup=None)
    print(yellow_text(get_time()), f"{message.chat.id}({red_text(message.from_user.username)}): '{message.text}'")
    
bot.polling(none_stop=True, timeout=200)