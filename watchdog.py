import os
from time import sleep
from includes import get_time
from sys import argv
# 
path_for_key = "/mnt/share/ТНГ"


while True:
	if os.path.isdir(path_for_key):
		# print("Everything allrignt")
	else:
		# print("Need to reboot!!!")
		f.open(f"log_{argv[0]}")
		f.write(f"At {get_time()}")
		f.close()
		os.system("reboot")
	sleep(10)