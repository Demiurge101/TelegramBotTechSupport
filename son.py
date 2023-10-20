import os
from Config import mkcb_location
from includes import get_access_to_path


son_text = {'begin':"Введите заводской номер изделия (номер в формате «300хххххххх»)\
 или децимальный номер изделия (номер после \"МКЦБ.\" в формате «хххххх.ххх» либо «хххххх.ххх-хх»). \r\n\
При вводе децимального номера Вам будут доступны только общие документы на конкретный класс изделий\
 (руководства, прошивки, схемы, сборочные чертежи  и др.), при вводе заводского номера Вам будут дополнительно\
  доступны скан-копии с печатями и подписями индивидуальных документов на конкретное изделие (паспорта, акты\
   опрессовки, акты калибровки и др.).",

   'wrong_number':"По указанному номеру изделий не найдено. Введите другой заводской или децимальный номер\
    изделия или нажмите кнопку «Назад», чтобы вернуться в корневое меню.",

    'wrong_code':"Введён некорректный шифр, введите корректный шифр документа. Введите заводской или децимальный\
     номер изделия, чтобы перейти к другому изделию или нажмите кнопку «Назад», чтобы вернуться в корневое меню.",

     'you_can_get_docs':"По указанному номеру Вам доступны следующие документы на изделие:",

     'enter_code_for_download':"Для скачивание необходимого документа Введите его шифр, указанный в скобках.",

     'another_code_or_number':"Введите другой шифр, чтобы загрузить другой документ по текущему изделию. Введите\
      заводской или децимальный номер изделия, чтобы перейти к другому изделию или нажмите кнопку «Назад», чтобы\
       вернуться в корневое меню."}


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

	def __getNumber(self, user_id, tn=0):
		if user_id in self.__users:
			return self.__users[user_id][tn]
		else:
			return ""

	def getDecimalNumber(self, user_id):
		self.__getNumber(user_id, 1)

	def getSerialNumber(self, user_id):
		self.__getNumber(user_id, 0)

	def getType(self, user_id):
		if user_id in self.__users:
			if self.__users[user_id][0]:
				return 'number'
			elif self.__users[user_id][1]:
				return 'mkcb'
		else:
			return ""

	def deleteSerialNumber(self, user_id):
		self.__users[user_id][0] = ""

	def setNumber(self, user_id, number):
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
		if not os.path.isdir(location):
			return [son_text['wrong_number']]
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
		if not os.path.isdir(location):
			return [son_text['wrong_number']]
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
			return [son_text['wrong_number']]
		result = []
		if self.getSerialNumber(user_id):
			result += self.__getSerialCodes(location)
		if self.getDecimalNumber(user_id):
			result += self.__getDecimalCodes(self.__mkcb_location + '\\' + self.getDecimalNumber(user_id))
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
