import pyautogui
import random
from random import choice
from time import sleep

main_buttons = [(1294, 714), (882, 709), (907, 803), (1329, 808)]
back_button = (1351, 820)

src = "./res/tester_src/"
back_button_img = "back.png"
main_buttons_img = ["kedr.png", "network.png", "soft.png", "son.png"]

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

def press_img(i):
	if pyautogui.click(i, duration=1):
		print("True")
	else:
		print("False")

while True:
	sleep(between_delay)
	# press(random.choice(main_buttons))
	press_img(src + random.choice(main_buttons_img))
	sleep(between_delay)
	press_img(src+back_button_img)