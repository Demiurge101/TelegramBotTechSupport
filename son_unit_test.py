from son import *
from includes import red_text, green_text

sn = SonController()


# unit 1

sn.setNumber(123456, '12345678')
sn.setNumber(123457, 'fw')
sn.setNumber(123458, '123456.123')
sn.setNumber(123459, '123456.123-12')
sn.setNumber(111111, '11223344')
sn.setNumber(111111, '44332211')
sn.setNumber(111111, '12345678t')

pattern1 = "id: 123456 = 12345678 (serial number)\r\n"
pattern1 += "id: 123458 = 123456.123 (decimal number)\r\n"
pattern1 += "id: 123459 = 123456.123-12 (decimal number)\r\n"
pattern1 += "id: 111111 = 44332211 (serial number)\r\n"



if sn.getUsersList() == pattern1:
	print(f"Unit 1: {green_text('Good!')}")
else:
	print(f"Unit 1: {red_text('Bad!')}")
	print(f"We're get \r\n'{sn.getUsersList()}'")
	print(f"Should be \r\n'{pattern1}'")
print()

# unit 2

sn.setNumber(1, '123456.789')
sn.setNumber(2, '123456.123')
sn.setNumber(3, '111666.999-01')
pattern2 = {}


unit2 = True
get = []
should = []
if ["Wrong location or can't find codes for this number"] != sn.getCodesMenu(1):
	unit2 = False
	get = sn.getCodesMenu(1)




if unit2:
	print(f"Unit 2: {green_text('Good!')}")
else:
	print(f"Unit 2: {red_text('Bad!')}")
	# print(f"We're get \r\n'{}'")
	# print(f"Should be \r\n'{}'")
print()