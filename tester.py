import pyautogui
import random
from random import choice
from time import sleep

main_buttons = [(1294, 714), (882, 709), (907, 803), (1329, 808)]
back_button = (1351, 820)

start_delay = 5
between_delay = 2

print("Start in ...")
for i in range(start_delay):
	print(start_delay - i)
	sleep(1)
print("Started.")

def press(c):
	# pyautogui.moveTo(c[0], c[1], duration=10)
	pyautogui.click(c[0], c[1], duration=1)


while True:
	sleep(between_delay)
	press(random.choice(main_buttons))
	sleep(between_delay)
	press(back_button)