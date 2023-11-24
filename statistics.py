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

	def getUsersInfo(self, detailed=False):
		res = ''
		count = 0
		for user in self.__users:
			count += 1
			req_info = f"({self.__users[user]['sum_requests']} requests, {round(self.__percent(self.__users[user]['sum_requests'], self.__sum_requests), 2)}%)"
			if detailed:
				count_req = 0
				for request in self.__users[user]['requests']:
					count_req += 1
					req_info += f"\r\n   {count_req}) {request}: {self.__users[user]['requests'][request]}"
			res += f"<b>{count}.</b> {user}:  <b>{self.__users[user]['username']}  {self.__users[user]['name']}</b>  {req_info}\r\n"
		return res

	def getRequestsInfo(self):
		res = ''
		count = 0
		for request in self.__requests:
			count += 1
			res += f"{count}) '{request}':  {self.__requests[request]}  ({round(self.__percent(self.__requests[request], self.__sum_requests), 2)}%)\r\n"
		return res

	def __percent(self, c, a):
		return c * 100 / a

	def getCountUsers(self):
		return len(self.__users)

	def getSum(self):
		return self.__sum_requests

	def save(self, fname='stat.txt'):
		pass

	def load(self, fname='stat.txt'):
		pass



		