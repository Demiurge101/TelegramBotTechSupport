import os

source_location = "./fileDB"
target_location = "./son"

def station_mkcb(name):
	m = os.path.abspath(name)
	print("-", m)
	# source_list = os.listdir(m)
	# for i in source_list:
	# 	print(i)

source_location = os.path.abspath(source_location)
target_location = os.path.abspath(target_location)
source_list = os.listdir(source_location)

for i in source_list:
	station_mkcb(i)

