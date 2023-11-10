import os
import MDataBase
import Config

source_location = Config.sonDBfiles
mkcb_location = Config.mkcb_location

clients = Config.clients


source_location = os.path.abspath(source_location)
source_list = os.listdir(source_location)

mkcb_location = os.path.abspath(mkcb_location)
mkcb_list = os.listdir(mkcb_location)

SN = MDataBase.SonDB(Config.db_host, Config.db_login, Config.db_password, Config.db_name_dispatcher_son)
SN.connect()

# add clients
for client in Config.clients:
	SN.addClient(client, Config.clients[client])

# parse mkcb
for folder_name in mkcb_list:
	if folder_name[:4] == 'МКЦБ':
		index = folder_name.find(' ')
		if index >= 0 and index < 19:
			mkcb_number = folder_name[:index]
			mkcb_name = folder_name[index+1:]
			print()
			print('mkcb number',mkcb_number)
			print(f"   mkcb name {mkcb_name}")
			SN.addMKCB(mkcb_number, mkcb_name, f'{mkcb_location}/{folder_name}'.replace('\\', '\\\\'))


# parse devices and stations
print()
for name in source_list:
	print(name) # org_name
	if (name in clients) == False:
		continue
	org_id = SN.getOrgIdByName(name) # org_id
	if org_id < 0:
		print("Нет организации с таким именем в базе данных. Добавьте организацию в БД и повторите попытку.")
		continue
	mn = os.path.abspath(source_location + '/' + name)
	list_dates = os.listdir(mn)
	for date in list_dates:
		print(" ", date) 
		dd = date[:2]
		mm = date[3:5]
		yy = date[6:]
		date_out = yy + "-" + mm + "-" + dd
		print(" ", date_out)  # date out
		md = os.path.abspath(mn + '/' + date)
		list_mkcb = os.listdir(md)
		for mkcb in list_mkcb:
			ind = mkcb.find("МКЦБ.")
			if ind > 0:
				print("  ", mkcb[ind:]) # station mkcb
				mm = os.path.abspath(md + '/' + mkcb)
				list_station_id = os.listdir(mm)
				for station_id in list_station_id:
					print("   ", station_id)  # station id
					msi = os.path.abspath(mm + '/' + station_id)

					# add station in bd
					msp = msi.find(name)
					# print("MSI: ", msi[msp:])
					station_location = "./" + msi[msp:]
					SN.addStation(station_id, name, mkcb[ind:], date_out, station_location.replace("\\", "\\\\"), "parsed")

					list_devices = os.listdir(msi)
					for device in list_devices:
						indm = device.find("МКЦБ.")
						indn = device.find(" ")
						if indm > 0:
							print("    ", device[indm:]) # device mkcb
							if indn > 0:
								print("    ", device[indn:indm]) # device name

								mdi = os.path.abspath(msi + "/" + device)
								list_devices_id = os.listdir(mdi)
								for device_id in list_devices_id:
									print("     ", device_id) # device id
									mdc = os.path.abspath(mdi + "/" + device_id)

									# add device in bd
									idp = mdc.find(name)
									# print(" MDC: ", mdc[idp:])
									device_location = "./" + mdc[idp:]
									SN.addDevice(device_id, station_id, name, device[indn:indm], device[indm:], date_out, device_location.replace("\\", "\\\\"), "parsed")


