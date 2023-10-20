import os
from Config import mkcb_location
from includes import get_access_to_path



class SonController():
	"""docstring for son"""
	def __init__(self):
		self.__mkcb_location = mkcb_location
		self.__users = {}
		get_access_to_path(self.__mkcb_location)
		self.__decimal_codes = {'сб' : "Сборочный чертёж (СБ)", 'сп' : "Спецификация (СП)",
		 'э' : "Схемы электрические (Э)", 'fw' : "Прошивка и инструкция по прошивке (FW)",
		 'рэ' : "Руководство по эксплуатации (РЭ)", 'сэр' : "Сертификаты и свидетельства (СЕР)",
		  'по' : "Программное обеспечение (ПО)", 'и' : "Прочие инструкции (И)"}
		self.__serial_codes = {'пс' : "Паспорт (ПС)", 'ао' : "Акт опрессовки (АО)",
		 'пк' : "Протокол калибровки (ПК)", 'пп' : "Протокол поверки (ПП)"}

	def getNumber(self, user_id):
		if user_id in self.__users:
			return self.__users[user_id][0]
		else:
			return ""

	def getType(self, user_id):
		if user_id in self.__users:
			return self.__users[user_id][1]
		else:
			return False

	def setNumber(self, user_id, number):
		parsed_type = self.parseType(number)
		if parsed_type == 'mkcb' or parsed_type == 'number':
			n_type = False
			if parsed_type == 'number':
				n_type = True
			self.__users[user_id] = (number, n_type)
		return parsed_type


	def addUser(self, user_id, number, n_type=False):
		self.__users[user_id] = (number, n_type)

	def parseType(self, number):
		number = number.lower()
		pp = number.find('.')
		if pp > -1:
			if pp == 6:
				if len(number) == 10 or len(number) == 13 and number.find('-') == 10:
					return 'mkcb'
			return 'w_mkcb'
		if len(number) == 8:
			try:
				int(number, 10)
				return "number"
			except Exception as e:
				pass
		if number in self.__decimal_codes:
			return 'd_code'
		elif number in self.__serial_codes:
			return 's_code'
		return "unknown"

	def __getDecimalCodes(self, location=''):
		result = []
		full_path = os.path.abspath(location)
		l_dirs = os.listdir(full_path)
		for fld in l_dirs:
			index = fld.find(' ')
			code = fld[:index].lower()
			if code in self.__decimal_codes:
				result.append(self.__decimal_codes[code])
		return result

	def __getSerialCodes(self, location=''):
		result = []
		full_path = os.path.abspath(location)
		l_dirs = os.listdir(full_path)
		for fld in l_dirs:
			index = fld.find(' ')
			code = fld[:index].lower()
			if code in self.__serial_codes:
				result.append(self.__serial_codes[code])
		return result

	def getCodesMenu(self, user_id, location='', mkcb=''):
		if not user_id in self.__users:
			return ["Неправильный номер"]
		result = []
		number_type = self.getType(user_id)
		if not location or number_type == False:
			location = self.__mkcb_location + '\\' + self.__users[user_id][0]
		if not os.path.isdir(location):
			return ["Wrong location or can't find codes for this number"]
		if number_type:
			self.__getSerialCodes(location)
			if not mkcb:
				return result
		if not mkcb:
			mkcb = self.__users[user_id][0]
		self.__getDecimalCodes(location)
		return result

	def getUsersList(self):
		result = ""
		for user in self.__users:
			t = "decimal"
			if self.__users[user][1]:
				t = "serial"
			result += f"id: {user} = {self.__users[user][0]} ({t} number)\r\n"
		return result
