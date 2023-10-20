import os
from Config import mkcb_location
from includes import get_access_to_path



class SonController():
	"""docstring for son"""
	def __init__(self):
		self.__mkcb_location = mkcb_location
		get_access_to_path(self.__mkcb_location)
		self.__decimal_codes = {'сб' : "Сборочный чертёж (СБ)", 'сп' : "Спецификация (СП)",
		 'э' : "Схемы электрические (Э)", 'fw' : "Прошивка и инструкция по прошивке (FW)",
		 'рэ' : "Руководство по эксплуатации (РЭ)", 'сэр' : "Сертификаты и свидетельства (СЕР)",
		  'по' : "Программное обеспечение (ПО)", 'и' : "Прочие инструкции (И)"}
		self.__serial_codes = {'пс' : "Паспорт (ПС)", 'ап' : "Акт опрессовки (АП)",
		 'пк' : "Протокол калибровки (ПК)", 'пп' : "Протокол поверки (ПП)"}

	def parse_type(self, number):
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
