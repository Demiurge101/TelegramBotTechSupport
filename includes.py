from telebot import types
import datetime
from time import sleep


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


markup_list = (buttonway(["Проблемы с оборудованием КЕДР", "Проблемы с сетью" ,"Проблемы с программами DCSoft", "Система одного номера"], "Reply") ,
                   buttonway(["УСО", "Пульт бурильщика", "Датчики", "Кабели", "Назад"], "Reply") ,
                   buttonway(["Wifi точки", "Камеры", "Ip адресса", "Ip телефоны и атс", "Назад"], "Reply")  ,
                   buttonway(["DSServer", " ", "DSPlot", "DSDevice", "Назад"], "Reply"))

back_button = types.ReplyKeyboardMarkup(True)
btn1 = types.KeyboardButton("Назад")
back_button.row(btn1)
# back_button = (buttonway(["Назад"], "Reply"))

markup_list_inline = (buttonway(["Ubiquiti", "TP-Link"], "Inline"),
                      buttonway(["Fanvil X4","Fanvil X1", "Yeastar S20", "Yeastar S50"], "Inline"),
                      buttonway(["Кабели датчиков ГТИ","Магистральные Кабели"], "Inline"),
                      buttonway(["УСО Exd PowerLine","УСО Exd WDSL", "УСО Exn WDSL"], "Inline"),
                      buttonway(["ПНД Exd PowerLine","ПНД Exd WDSL", "ПНД Exn WDSL"], "Inline"),
                      buttonway(["ДНК","ДДИ", "ДУП", "РУД", "ДОП-М", "БЗУД", "ДТ"], "Inline"),
                    )

document_type = {".pdf", ".txt", ".bin", ".doc", ""}
image_type = {".img", ".png", ".bmp"}
video_type = {".mp4"}
audio_type = {".mp3"}

return_keys = {"/cancel", "/back", "назад", "Назад"}

start_text = "Добро пожаловать в бот технической поддержки ГеоФизМаш. Он предназначен для нахождения быстрых ответов, на самые распространённые проблемы. Для полного списка комманд введите /help"


def get_time():
  return datetime.datetime.now().strftime("<%Y-%m-%d, %H:%M:%S.%f")[:-3]+">"