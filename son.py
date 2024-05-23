import os
from Config import mkcb_location
from includes import get_access_to_path, checkFiles


son_text = {'begin':"Введите <b>заводской</b> номер изделия (номер в формате «<b><u>300хххххххх</u></b>») или <b>децимальный</b> номер изделия (номер после \"<u><b>МКЦБ.</b></u>\" в формате <u>«<b>хххххх.ххх</b>» либо «<b>хххххх.ххх-хх</b>»</u>). \r\n\
<i>При вводе <b>децимального</b> номера Вам будут доступны только <b>общие</b> документы на конкретный <b>класс изделий</b> (руководства, прошивки, схемы, сборочные чертежи  и др.), при вводе <b>заводского</b> номера Вам будут дополнительно доступны скан-копии с печатями и подписями <b>индивидуальных</b> документов на <b>конкретное</b> изделие (паспорта, акты опрессовки, акты калибровки и др.).</i>",

   'wrong_number':"По указанному номеру изделий не найдено. Введите другой <b>заводской</b> или <b>децимальный</b> номер изделия или нажмите кнопку «Назад», чтобы вернуться в корневое меню.",

    'wrong_code':"Введён некорректный шифр, введите корректный шифр документа. Введите <b>заводской</b> или <b>децимальный</b> номер изделия, чтобы перейти к другому изделию или нажмите кнопку «Назад», чтобы вернуться в корневое меню.",

     'you_can_get_docs':"По указанному номеру Вам доступны следующие документы на изделие:",

     'enter_code_for_download':"Для скачивание необходимого документа Введите его шифр, указанный в скобках.",

     'another_code_or_number':"Введите другой шифр, чтобы загрузить другой документ по текущему изделию. Введите <b>заводской</b> или <b>децимальный</b> номер изделия, чтобы перейти к другому изделию или нажмите кнопку «Назад», чтобы вернуться в корневое меню."}


class SonController():
	"""docstring for son"""
	def __init__(self):
		self.__mkcb_location = mkcb_location
		self.__users = {}
		self.__locations = {}
		get_access_to_path(self.__mkcb_location)
		self.__decimal_codes = {
			'сер' : "Сертификаты и свидетельства (СЕР)",
			'сб' : "Сборочный чертёж (СБ)",
			'сп' : "Спецификация (СП)",
			'fw' : "Прошивка и инструкция по прошивке (FW)",
			'рэ' : "Руководство по эксплуатации (РЭ)",
			'по' : "Программное обеспечение (ПО)",
			'э' : "Схемы электрические (Э)",
			'и' : "Прочие инструкции (И)"
		}
		self.__serial_codes = {
			'пс' : "Паспорт (ПС)",
			'ао' : "Акт опрессовки (АО)",
			'пк' : "Протокол калибровки (ПК)",
			'пп' : "Протокол поверки (ПП)"
		}

	def getLocation(self):
		return self.__mkcb_location

	def setUserLocation(self, user_id, location=''):
		if location:
			self.__locations[user_id] = location

	def getUserLocation(self, user_id):
		if user_id in self.__locations:
			return self.__locations[user_id]
		return ''

	def deleteUserLocation(self, user_id):
		if user_id in self.__locations:
			del self.__locations[user_id]

	def __getNumber(self, user_id, tn=0):
		if user_id in self.__users:
			return self.__users[user_id][tn]
		else:
			return ""

	def getDecimalNumber(self, user_id):
		return self.__getNumber(user_id, 1)

	def getSerialNumber(self, user_id):
		return self.__getNumber(user_id, 0)

	def getType(self, user_id):
		if user_id in self.__users:
			if self.__users[user_id][0]:
				return 'number'
			elif self.__users[user_id][1]:
				return 'mkcb'
			else:
				return ""
		else:
			return ""

	def deleteSerialNumber(self, user_id):
		if user_id in self.__users:
			self.__users[user_id][0] = ""

	def setNumber(self, user_id, number):
		print(number)
		number = str(number)
		parsed_type = self.parseType(number)
		if user_id in self.__users:
			if parsed_type == 'mkcb':
				self.__users[user_id][1] = number
			if parsed_type == 'number':
				self.__users[user_id][0] = number
		else:
			if parsed_type == 'mkcb':
				self.__users[user_id] = ["", number]
			if parsed_type == 'number':
				self.__users[user_id] = [number, ""]
		return parsed_type


	def addUser(self, user_id, device="", mkcb=""):
		self.__users[user_id] = [device, mkcb]

	def deleteUser(self, user_id):
		if user_id in self.__users:
			del self.__users[user_id]

	def parseType(self, number):
		number = number.lower()
		pp = number.find('.')
		if pp > -1:
			if pp == 6:
				if len(number) == 10 or len(number) == 13 and number.find('-') == 10:
					return 'mkcb'
			return 'w_mkcb'
		# if len(number) == 8:
		if len(number) >= 5 and len(number) <= 10:
			try:
				int(number, 10)
				return "number"
			except Exception as e:
				pass
		if number in self.__decimal_codes:
			return 'd_code'
		elif number in self.__serial_codes:
			return 's_code'
		elif self.__inverseCode(number) in self.__decimal_codes:
			return 'd_icode'
		elif self.__inverseCode(number) in self.__serial_codes:
			return 's_icode'
		return "unknown"

	def getTextByCode(self, code):
		print(f"getTextByCode({code})") #debug
		for i in code: #debug
			print(f"{i}: {ord(i)}") #debug
		if code in self.__decimal_codes:
			return self.__decimal_codes[code]
		elif code in self.__serial_codes:
			return self.__serial_codes[code]
		return '-'

	def __inverseCode(self, code=''):
		# print(yellow_text(f"__inverseCode({code})"))
		en_alphabet = "qwertyuiop[]asdfghjkl;'zxcvbnm,.`"
		ru_alphabet = "йцукенгшщзхъфывапролджэячсмитьбюё"
		res = ''
		for c in code:
			index = ru_alphabet.find(c)
			if index >= 0:
				res += en_alphabet[index]
				continue
			index = en_alphabet.find(c)
			if index >= 0:
				res += ru_alphabet[index]
		return res

	def inverseCode(self, code=''):
		return self.__inverseCode(code)

	def __getDecimalCodes(self, location=''):
		result = []
		# print('__getDecimalCodes()')
		if not os.path.isdir(location):
			return []
		# print('is dir')
		full_path = os.path.abspath(location)
		l_dirs = os.listdir(full_path)
		# print('search...')
		for fld in l_dirs:
			index = fld.find(' ')
			code = fld[:index].lower()
			if code in self.__decimal_codes:
				# print(f"--code: {code}")
				if checkFiles(full_path + '/' + fld):
					# print(f'append {self.__decimal_codes[code]}')
					result.append(self.__decimal_codes[code])
		return result

	def __getSerialCodes(self, location=''):
		result = []
		if not os.path.isdir(location):
			return []
		full_path = os.path.abspath(location)
		l_dirs = os.listdir(full_path)
		for fld in l_dirs:
			index = fld.find(' ')
			code = fld[:index].lower()
			if code in self.__serial_codes:
				if checkFiles(full_path + '/' + fld):
					result.append(self.__serial_codes[code])
		return result

	def getCodes(self, user_id, location='', mkcb_location=''):
		# print('location: ', location)
		# print('mkcb location', mkcb_location)
		# print("Users:")
		# print(self.__users)
		# print('.')
		if not user_id in self.__users:
			# print("user not in")
			return [son_text['wrong_number']]
		result = []
		if self.getSerialNumber(user_id):
			if not location:
				if user_id in self.__locations:
					location = self.__locations[user_id]
			result += self.__getSerialCodes(location)
		if self.getDecimalNumber(user_id):
			# result += self.__getDecimalCodes(self.__mkcb_location + '/' + self.getDecimalNumber(user_id))
			result += self.__getDecimalCodes(mkcb_location)
		return result

	def getUsersList(self):
		result = ""
		for user in self.__users:
			t = "decimal"
			number = ""
			if self.__users[user][0]:
				t = "serial"
				number = self.__users[user][0]
			else:
				number = self.__users[user][1]
			result += f"id: {user} = {number} ({t} number)\r\n"
		return result
