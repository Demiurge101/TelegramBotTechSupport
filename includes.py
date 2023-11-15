from telebot import types
import datetime
from time import sleep
import os
import colorama
from colorama import Fore, Back, Style
colorama.init()
from getpass import getpass
import subprocess
from sys import platform

operating_system = 'unknown'

if platform == "linux" or platform == "linux2":
  operating_system = 'linux'
elif platform == "darwin":
  operating_system = 'x'
elif platform == "win32":
  operating_system = 'windows'

print(f"OS: {operating_system}")

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

document_type = {".pdf", ".txt", ".bin", ".doc", ".docx", ".zip", ".rar", ".7z", ""}
image_type = {".img", ".png", ".bmp", ".jpg"}
video_type = {".mp4"}
audio_type = {".mp3"}

return_keys = {"/cancel", "/back", "назад", "Назад"}


def get_time():
  return datetime.datetime.now().strftime("<%Y-%m-%d, %H:%M:%S.%f")[:-3]+">"


def red_text(text):
  return Fore.RED + text + Style.RESET_ALL

def blue_text(text):
  return Fore.BLUE + text + Style.RESET_ALL

def green_text(text):
  return Fore.GREEN + text + Style.RESET_ALL

def yellow_text(text):
  return Fore.YELLOW + text + Style.RESET_ALL


def get_access_to_path(path, user = ""):
  backup_storage_available = os.path.isdir(path)
  if backup_storage_available:
      print("Storage already connected.")
      print(path)
  else:
      print(f"Connecting to {path}.")
      if not user:
        user = input("User: ")
      password = getpass("Password: ")
      print ("\033[A                                                         \033[A")
      if operating_system == 'windows':
        mount_command = f"net use /user:\"{user}\" \"{path}\" \"{password}\""
        os.system(mount_command)
      elif operating_system == 'linux':
        mount_command = f'sudo mount.cifs {path}, /home/ad/share -o user={user}'
        os.system(mount_command)
      backup_storage_available = os.path.isdir(path)
      if backup_storage_available:
          print(f"Connection success.")
      else:
          print(f"Failed to find {path}.")


def checkFiles(location, rec=True, is_first=True):
  try:
    source_location = os.path.abspath(location)
    if os.path.isfile(source_location):
      file_type = os.path.splitext(source_location)
      if file_type[-1] in document_type or file_type[-1] in image_type or file_type[-1] in video_type or file_type[-1] in audio_type or file_type[-1] == '.lnk':
        return True
      else:
        return False
    if rec == False and is_first == False:
      return False
    source_list = os.listdir(source_location)
    for i in source_list:
      if checkFiles(source_location + "/" + i, rec, False):
        # print(f"{source_location}/{i} - have files")
        return True
      # else:
        # print(f"{source_location}/{i} - don't have files")
  except Exception as e:
    print(f"Error: checkFiles({location}, {rec}, {is_first}) = {e}")
  return False


def check_symbols(ch):
  if ch > 127 and ch < 176:
    return ch + 912
  elif ch > 223 and ch < 240:
    return ch + 864
  elif ch == 240:
    return 1025
  elif ch == 241:
    return 1105
  return ch

def getLinkSource(link_path) -> (str):
    """
    Get the target & args of a Windows shortcut (.lnk)
    :param link_path: The Path or string-path to the shortcut, e.g. "C:/Users/Public/Desktop/My Shortcut.lnk"
    :return: A tuple of the target and arguments, e.g. ("C:/Program Files/My Program.exe", "--my-arg")
    """
    # get_target implementation by hannes, https://gist.github.com/Winand/997ed38269e899eb561991a0c663fa49
    if operating_system == 'windows':
      ps_command = \
          "$WSShell = New-Object -ComObject Wscript.Shell;" \
          "$Shortcut = $WSShell.CreateShortcut(\"" + str(link_path) + "\"); " \
          "Write-Host $Shortcut.TargetPath ';' $shortcut.Arguments "
      output = subprocess.run(["powershell.exe", ps_command], capture_output=True)
      raw = ''
      for i in output.stdout:
        raw += chr(check_symbols(i))
      launch_path, args = [x.strip() for x in raw.split(';', 1)]
      return launch_path
    elif operating_system == 'linux':
      return link_path
    return ''