import os
import MDataBase
import Config
from sys import argv
from getpass import getpass
from includes import *


version = "v.2.0"

author = "parser_son_db"
log_file = "son_parser_log.txt"
rewrite = False

parse_mkcb = True
parse_devices = True
check_err = False
logs = True




common_location = Config.common_location
source_location = Config.sonDBfiles
mkcb_location = Config.mkcb_location
# common_location = Config.uuid_files_location

host = Config.db_host
port = Config.db_port
login = Config.db_login
password = Config.db_password


for i in argv:
	if i == '-f': # foreign database
		host = input("host (and port): ")
		index = host.find(':')
		if index >= 0:
			port = int(host[index+1:])
			host = host[:index]
		login = input('login: ')
		password = getpass('password: ')
	elif i == '-rw':
		rewrite = True
	elif i == "--disable_mkcb":
		parse_mkcb = False
	elif i == "--disable_devices":
		parse_devices = False
	elif i == "--check_err":
		check_err = True
	elif i == "--help":
		help_text = f"Version {version}\n"
		help_text += f"-f: foreign database\n"
		help_text += f"-rw: rewrite files\n"
		help_text += f"--disable_mkcb\n"
		help_text += f"--disable_devices\n"
		help_text += f"--check_err: pause on some errors\n"
		print(help_text)
		quit()

clients = Config.clients




path_list = {}



source_location = os.path.abspath(source_location)
source_list = os.listdir(source_location)

# common_location = os.path.abspath(common_location)

SN = MDataBase.SonDB(host, login, password, Config.db_name_dispatcher_son)
SN.connect()
SN.set_logs(logs)
SN.set_stop_errors(check_err)



# add clients
for client in Config.clients:
	SN.addClient(client, Config.clients[client])



def add_file(parent_number, file_type, file_location, file_name, rewrite=False):
	try:
		global SN
		global path_list
		global author
		index = file_name.rfind('.')
		if index >= 0 and file_name[index:] == '.lnk':
			location = getLinkSource(f"{file_location}/{file_name}")
			if location[0] == '.':
				location = common_location + location[1:]
			print(green_text(f"LOCATION: {location}"))
			# it should be file not dir
			# if parent_number == 'МКЦБ.611137.101-18':
			# 	textlog = f"location: {location} \n"
			# 	textlog += f"in path list: {location in path_list}\n\n"
			# 	fl = open("log_611137.101-18", 'w+')
			# 	fl.write(textlog)
			# 	fl.close()
			if location in path_list:
				fl_key = False
				files = SN.get_files(parent_number, file_type)
				for file in files:
					if file['namef'] == file_name:
						fl_key = True
						break
				if fl:
					SN.add_file_bond(parent_number, path_list[location])
					print(green_text(f"From {file_location}/{file_name}, get ({location}, {path_list[location]})"))
					# if parent_number == "МКЦБ.611139.102-04":
					# 	input("МКЦБ.611139.102-04")
			else:
				i_loc = location.rfind('/')
				uuid = SN.add_file_from_location(parent_number, file_type, location[:i_loc], location[i_loc+1:], rewrite=False)
				if uuid[:3] != "err":
					path_list[location] = uuid
		else:
			SN.add_file_from_location(parent_number, file_type, file_location, file_name, author, rewrite=False)
	except Exception as e:
		print(red_text("Error! (file)"), e)
		f = open(log_file, 'a')
		f.write(f"{e}\r\n\r\n")
		f.close()
		if check_err:
			input("error...")







#		   parse mkcb
if parse_mkcb:
	mkcb_location = os.path.abspath(mkcb_location)
	mkcb_list = os.listdir(mkcb_location)
	for folder_name in mkcb_list:
		if folder_name[:4] == 'МКЦБ':
			index = folder_name.find(' ')
			if index >= 0 and index < 19:
				mkcb_number = folder_name[:index]
				mkcb_name = folder_name[index+1:]
				print()
				print('mkcb number:',mkcb_number)
				print(f"   mkcb name: {mkcb_name}")
				SN.addMKCB(mkcb_number, mkcb_name)
				for subfolder in os.listdir(mkcb_location + '/' + folder_name):
					print(f"	  -subfolder: {subfolder}")
					if os.path.isdir(mkcb_location + '/' + folder_name + '/' + subfolder):
						print(f"	   is dir")
						index = subfolder.find(' ')
						if index >= 0:
							typef = subfolder[:index]
							location = os.path.abspath(mkcb_location + '/' + folder_name + '/' + subfolder)
							for file in os.listdir(location):
								print(f"		 file: {file}")
								print(f"abspath: {location}")
								# print(yellow_text(file))
								add_file(mkcb_number, typef, location, file, rewrite=rewrite)
								



for p in path_list:
	print(blue_text(f"{p}: {path_list[p]}"))




# parse devices and stations
def parse_device_mkcb(folder_name, folder_location, station_id, org_name, date_out):
	try:
		global SN
		folder_devices = os.path.abspath(f"{folder_location}/{folder_name}")
		print()
		print(f"Parse device: {folder_devices}")
		# index_mkcb = location.find("МКЦБ.")
		# index_first_space = location.find(' ')
		mkcb_params = folder_name.split()
		# len_mkcb_params = len(mkcb_params)
		mkcb = mkcb_params[len(mkcb_params)-1]
		name = mkcb_params[len(mkcb_params)-2]

		list_devices = os.listdir(folder_devices)
		for serial_number in list_devices:
			device_folder = os.path.abspath(f"{folder_devices}/{serial_number}")
			SN.addDevice(serial_number, station_id, org_name, name, mkcb, date_out, description=author)
			list_types = os.listdir(device_folder)
			for folder_type in list_types:
				types_folder = os.path.abspath(f"{device_folder}/{folder_type}")
				type_params = folder_type.split()
				typef = type_params[0]
				files = os.listdir(types_folder)
				for file in files:
					# print("-abspath")
					# print(os.path.abspath(file))
					# index = file.find('.')
					# print(yellow_text(file))
					# if index >= 0:
					# 	if file[index:] != '.lnk':
							# types_folder = getLinkSource(f"{types_folder}/{file}")
					add_file(serial_number, typef, types_folder, file, rewrite=rewrite)
	except Exception as e:
		print(red_text("Error! (device)"), e)
		f = open(log_file, 'a')
		f.write(f"{e}\r\n\r\n")
		f.close()




def parse_station_mkcb(org_name, date_out, mkcb, mkcb_folder):
	try:
		global SN
		numbers_folder = os.path.abspath(f"{mkcb_folder}/{mkcb}")
		print()
		print(f"Parse station: {numbers_folder}")
		mkcb_params = mkcb.split()
		numbers = os.listdir(numbers_folder)
		decimal_number = mkcb_params[len(mkcb_params) - 1]
		it = 0
		for i in mkcb_params:
			if i[:4] == 'МКЦБ':
				decimal_number = mkcb_params[it]
			it += 1
		for number in numbers:
			devices_folder = os.path.abspath(f"{numbers_folder}/{number}")
			if os.path.isdir(devices_folder):
				SN.addStation(number, org_name, decimal_number, date_out, description=author)
				devices = os.listdir(devices_folder)
				for device in devices:
					# print("-----", device)
					device_folder = os.path.abspath(f"{devices_folder}/{device}")
					if device.find("МКЦБ") >= 0:
						parse_device_mkcb(device, devices_folder, number, org_name, date_out)
					else:
						file_params = device.split()
						typef = file_params[0]
						for file in os.listdir(device_folder):
							# print(f"device_folder: {device_folder}")
							# print(f"file: {file}")
							# print(yellow_text(file))
							# index = file.find('.')
							# if index > -1 and file[index:] != '.lnk':
								# types_folder = getLinkSource(f"{location}/{file}")
							add_file(number, typef, device_folder, file, rewrite=rewrite)
	except Exception as e:
		print(red_text("Error! (station)"), e)
		f = open(log_file, 'a')
		f.write(f"{e}\r\n\r\n")
		f.close()


if parse_devices:
	print()
	key_id = 0
	for org_name in source_list:
		print(org_name) # org_name
		# if (org_name in clients) == False:
		# 	continue
		org_id = SN.getOrgIdByName(org_name) # org_id
		if org_id < 0:
			print("Нет организации с таким именем в базе данных. Добавьте организацию в БД и повторите попытку.")
			# continue
			pwd = org_name
			if len(pwd) > 7:
				pwd = pwd[:7]
			SN.addOrg(org_name, f"ga1n-{pwd}")
			# key_id += 1
		mn = os.path.abspath(source_location + '/' + org_name)
		list_dates = os.listdir(mn)
		for date_folder in list_dates:
			print(" ", date_folder) 
			dd = date_folder[:2]
			mm = date_folder[3:5]
			yy = date_folder[6:]
			date_out = yy + "-" + mm + "-" + dd
			print(" ", date_out)  # date out
			mkcb_folder = os.path.abspath(mn + '/' + date_folder)
			list_mkcb = os.listdir(mkcb_folder)
			for mkcb in list_mkcb:
				if mkcb.lower().find("станция") >= 0:
					parse_station_mkcb(org_name, date_out, mkcb, mkcb_folder)
				else:
					# location = os.path.abspath(f"{mkcb_folder}/{mkcb}")
					parse_device_mkcb(mkcb, mkcb_folder, None, org_name, date_out)
				


SN.delete_dub_filebonds()
SN.delete_links_from_db()
	