from son import *
from includes import red_text, green_text
from unit_test import Unit

sn = SonController()


# unit 1
u1 = Unit(1)

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



u1.test(sn.getUsersList(), pattern1)
u1.result()

# unit 2
sn = SonController()
sn.setNumber(1, '12345678')
sn.setNumber(2, '12345678')
sn.setNumber(2, 87654321)
sn.setNumber(2, '123456.789')

sn.setNumber(3, '112233.123-02')
sn.setNumber(3, '11223344')


sn.deleteSerialNumber(1)
u2 = Unit(2)
u2.test(sn.getSerialNumber(1), "")
u2.test(sn.getDecimalNumber(1), "")
u2.test(sn.getType(1), "")

u2.test(sn.getSerialNumber(2), "87654321")
u2.test(sn.getDecimalNumber(2), "123456.789")
u2.test(sn.getType(2), "number")

u2.test(sn.getSerialNumber(3), "11223344")
u2.test(sn.getDecimalNumber(3), "112233.123-02")
u2.test(sn.getType(3), "number")

sn.deleteSerialNumber(3)
u2.test(sn.getSerialNumber(3), "")
u2.test(sn.getDecimalNumber(3), "112233.123-02")
u2.test(sn.getType(3), "mkcb")

u2.result()

























sn.setNumber(1, '123456.789')
sn.setNumber(2, '123456.123')
sn.setNumber(3, '111666.999-01')
sn.setNumber(4, '11223344')
sn.setNumber(5, '12345678')
sn.setNumber(5, '123456.136')

# print(1, sn.getCodes(1))
# print(2, sn.getCodes(2))
# print(3, sn.getCodes(3))
# print(4, sn.getCodes(4))
# print(5, sn.getCodes(5))
# print(6, sn.getCodes(6))