from datetime import datetime



class Statistics():
	"""docstring for Statistics"""
	def __init__(self):
		self.__users = {}
		self.__requests = {}

	def __add_user(self, user_id, name=None, username=None):
		self.__users[user_id] = {'name' : name, 'username' : username, 'requests' : {}}

	def __add_request(self, user_id, request):
		if request in self.__users[user_id]['requests']:
			self.__users[user_id]['requests'][request] += 1
		else:
			self.__users[user_id]['requests'][request] = 1

	def fromMessage(self, m):
		# print(f"about user: {m.from_user}")
		if not m.from_user.id in self.__users:
			name = f"{m.from_user.first_name} {m.from_user.last_name}"
			self.__add_user(m.from_user.id, name, m.from_user.username)
		self.__add_request(m.from_user.id, m.text)
		if not m.text in self.__requests:
			self.__requests[m.text] = 1
		else:
			self.__requests[m.text] += 1

	def getUsersInfo(self):
		res = ''
		for user in self.__users:
			res += f"{user}: {self.__users[user]['username']} {self.__users[user]['name']} ({len(self.__users[user]['requests'])} requests)\r\n"
		return res

	def getRequestsInfo(self):
		res = ''
		for request in self.__requests:
			res += f"'{request}':{self.__requests[request]}\r\n"
		return res



		