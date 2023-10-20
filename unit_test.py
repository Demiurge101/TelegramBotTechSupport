from includes import green_text, red_text


class Unit():
	"""docstring for Unit"""
	def __init__(self, name="_", description=""):
		self.__name = f"Unit {name}"
		self.__description = description
		self.__result_gets = []
		self.__result_patterns = []

	def test(self, get, pattern):
		if get != pattern:
			self.__result_gets.append(get)
			self.__result_patterns.append(pattern)

	def result(self):
		d = ""
		if self.__description:
			d = f" ({self.__description})"
		if self.__result_gets or self.__result_patterns:
			print(f"{self.__name}{d}: {red_text('Bad!')}")
			ln = len(self.__result_gets)
			if len(self.__result_patterns) > ln:
				ln = len(self.__result_patterns)
			for i in range(ln):
				print(f"We're get: \r\n'{self.__result_gets[i]}'\r\nShould be: \r\n'{self.__result_patterns[i]}'\r\n")
		else:
			print(f"{self.__name}{d}: {green_text('Good!')}")
		print()
		