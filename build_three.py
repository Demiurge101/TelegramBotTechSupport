import os
import MDataBase
import Config

root_location = Config.tsDBfiles
content_file_type = ".cnt"



# TS = MDataBase.TSDB("localhost", "root", Config.password, Config.bd_name_dispatcher_ts)
TS = MDataBase.TSDB("localhost", "root", Config.password, "TS_Dispatcher_test")
TS.connect()


def makeNode(location, title = "", parent_id=0):
	source_location = None
	if title == "":
		source_location = os.path.abspath(location)
	else:
		source_location = os.path.abspath(location + "\\" + title)
	# print(source_location)
	if os.path.isfile(source_location):
		if source_location[-4:] == content_file_type:
			f = open(source_location, 'r')
			data = f.read()
			f.close()
			content = TS.getContent(parent_id)
			if content:
				TS.setContentText(parent_id, data)
			else:
				TS.addContent(parent_id, data)
			print(data)
		return
	print(source_location)
	title_id = parent_id
	if title != "":
		title_id = TS.getIdByTitle(title)
		if title_id >= 0:
			# update here
			content = TS.getContent(title_id)
			if content:
				TS.setContentLocation(title_id, source_location)
			else:
				TS.addContent(title_id, title, source_location)
		else:
			TS.addTitle(parent_id, title, 1)
			title_id = TS.getIdByTitle(title)
			TS.addContent(title_id, title, source_location)

	source_list = os.listdir(source_location)
	for i in source_list:
		makeNode(source_location, i, title_id)




# root_location = os.path.abspath(location)
# if os.path.isdir(root_location):
# 	root_list = os.listdir(root_location)
# 	for i in root_list:
# 		makeNode(root_location + "\\" + i)

makeNode(root_location)