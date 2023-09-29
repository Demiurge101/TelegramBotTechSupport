import threading

def thread(func, args):
	try:
		th = threading.Thread(target=func, args=args)
		th.start()
	except Exception as e:
		print("Error in thread")
		print(e)
	




# @bot.message_handler(commands=['start'])
# def start_command_handler(message):
#     chat_id = message.chat.id
#     t = threading.Thread(target=send_numbers, args=(chat_id,))
#     t.start()


# @bot.message_handler(commands=['stop'])
# def stop_command_handler(message):
#     for t in threading.enumerate():
#         if t.getName() == str(message.chat.id):
#             t.do_run = False
#             t.join()