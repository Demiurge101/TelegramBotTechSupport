import os
import MDataBase
import Config
from sys import argv
from getpass import getpass

source_location = Config.sonDBfiles
mkcb_location = Config.mkcb_location
# common_location = Config.uuid_files_location

host = Config.db_host
login = Config.db_login
password = Config.db_password


for i in argv:
	if i == '-f': # foreign database
		host = input("host: ")
		login = input('login: ')
		password = getpass('password: ')

clients = Config.clients


source_location = os.path.abspath(source_location)
source_list = os.listdir(source_location)

mkcb_location = os.path.abspath(mkcb_location)
mkcb_list = os.listdir(mkcb_location)

# common_location = os.path.abspath(common_location)

SN = MDataBase.SonDB(host, login, password, Config.db_name_dispatcher_son)
SN.connect()



# add clients
for client in Config.clients:
	SN.addClient(client, Config.clients[client])












#           parse mkcb
for folder_name in mkcb_list:
	if folder_name[:4] == 'МКЦБ':
		index = folder_name.find(' ')
		if index >= 0 and index < 19:
			mkcb_number = folder_name[:index]
			mkcb_name = folder_name[index+1:]
			print()
			print('mkcb number:',mkcb_number)
			print(f"   mkcb name: {mkcb_name}")
			SN.addMKCB(mkcb_number, mkcb_name, "uuid")
			for subfolder in os.listdir(mkcb_location + '/' + folder_name):
				print(f"      -subfolder: {subfolder}")
				if os.path.isdir(mkcb_location + '/' + folder_name + '/' + subfolder):
					print(f"       is dir")
					index = subfolder.find(' ')
					if index >= 0:
						typef = subfolder[:index]
						location = os.path.abspath(mkcb_location + '/' + folder_name + '/' + subfolder)
						for file in os.listdir(location):
							print(f"         file: {file}")
							print(f"abspath: {location}")
							SN.add_file_from_location(mkcb_number, typef, location, file, "parser_son_db")












# parse devices and stations
def parse_device_mkcb(folder_name, folder_location, station_id, org_name, date_out):
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
		SN.addDevice(serial_number, station_id, org_name, name, mkcb, date_out, "uuid", "parser_son_db")
		list_types = os.listdir(device_folder)
		for folder_type in list_types:
			types_folder = os.path.abspath(f"{device_folder}/{folder_type}")
			type_params = folder_type.split()
			typef = type_params[0]
			files = os.listdir(types_folder)
			for file in files:
				# print("-abspath")
				# print(os.path.abspath(file))
				SN.add_file_from_location(serial_number, typef, types_folder, file, "parser_son_db")



def parse_station_mkcb(org_name, date_out, mkcb, mkcb_folder):
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
			SN.addStation(number, org_name, decimal_number, date_out, "uuid", "parser_son_db")
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
						SN.add_file_from_location(number, typef, device_folder, file, "parser_son_db")


print()
for org_name in source_list:
	print(org_name) # org_name
	if (org_name in clients) == False:
		continue
	org_id = SN.getOrgIdByName(org_name) # org_id
	if org_id < 0:
		print("Нет организации с таким именем в базе данных. Добавьте организацию в БД и повторите попытку.")
		continue
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
			



	