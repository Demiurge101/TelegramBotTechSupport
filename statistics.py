from datetime import datetime



class Statistics():
	"""docstring for Statistics"""
	def __init__(self):
		self.__users = {}
		self.__requests = {}
		self.__sum_requests = 0

	def __add_user(self, user_id, name=None, username=None):
		self.__users[user_id] = {'name' : name, 'username' : username, 'requests' : {}, 'sum_requests' : 0}

	def __add_request(self, user_id, request):
		self.__users[user_id]['sum_requests'] += 1
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
		self.__sum_requests += 1
		if not m.text in self.__requests:
			self.__requests[m.text] = 1
		else:
			self.__requests[m.text] += 1

	def getUsersInfo(self):
		res = ''
		for user in self.__users:
			req_info = f"({self.__users[user]['sum_requests']} requests, {round(self.__percent(self.__users[user]['sum_requests'], self.__sum_requests), 2)}%)"
			res += f"{user}: <b>{self.__users[user]['username']} {self.__users[user]['name']}</b> {req_info}\r\n"
		return res

	def getRequestsInfo(self):
		res = ''
		for request in self.__requests:
			res += f"'{request}': {self.__requests[request]} ({round(self.__percent(self.__requests[request], self.__sum_requests), 2)}%)\r\n"
		return res

	def __percent(self, c, a):
		return c * 100 / a

	def getSum(self):
		return self.__sum_requests

	def save(self, fname='stat.txt'):
		pass

	def load(self, fname='stat.txt'):
		pass



		