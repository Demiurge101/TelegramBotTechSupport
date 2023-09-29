import os
import MDataBase
import Config
from includes import *

root_location = Config.tsDBfiles
content_file_type = ".cnt"



TS = MDataBase.TSDB("localhost", "root", Config.password, Config.bd_name_dispatcher_ts)
# TS = MDataBase.TSDB("localhost", "root", Config.password, "TS_Dispatcher")
TS.connect()


def makeNode(location, title = "", parent_id=0):
	source_location = None
	if title == "":
		source_location = os.path.abspath(location)
	else:
		source_location = os.path.abspath(location + "\\" + title)
	# print(source_location)
	if os.path.isfile(source_location):
		file_atr = os.path.splitext(title)
		if file_atr[1] == content_file_type:
			f = open(source_location, 'r')
			data = f.read()
			f.close()
			content = TS.getContent(parent_id)
			if content:
				TS.setContentText(parent_id, data)
			else:
				TS.addContent(parent_id, data)
			print(data)
			if file_atr[0].lower() == "none" or file_atr[0].lower() == "null":
				TS.deleteTitleCommand(parent_id)
			else:
				TS.setTitleCommand(parent_id, f"/{file_atr[0]}")
		return
	print(source_location)
	have_files = checkFiles(source_location, False)
	title_id = parent_id
	if title != "":
		title_id = TS.getIdByTitle(title)
		if title_id >= 0: # if title exist
			# update here
			content = TS.getContent(title_id)
			if content:   # if content exist
				if have_files:
					TS.setContentLocation(title_id, source_location)
			else:         # if content doesn't exist
				if have_files:
					TS.addContent(title_id, title, source_location)
				else:
					TS.addContent(title_id, title)
		else:
			TS.addTitle(parent_id, title, 1)
			title_id = TS.getIdByTitle(title)
			if have_files:
				TS.addContent(title_id, title, source_location)
			else:
				TS.addContent(title_id, title)

	source_list = os.listdir(source_location)
	for i in source_list:
		makeNode(source_location, i, title_id)



def checkFiles(location, rec=True, is_first=True):
	source_location = os.path.abspath(location)
	if os.path.isfile(source_location):
		file_type = os.path.splitext(source_location)
		if file_type[-1] in document_type or file_type[-1] in image_type or file_type[-1] in video_type or file_type[-1] in audio_type:
			return True
		else:
			return False
	if rec == False and is_first == False:
		return False
	source_list = os.listdir(source_location)
	for i in source_list:
		if checkFiles(source_location + "\\" + i, rec, False):
			return True
	return False
# root_location = os.path.abspath(location)
# if os.path.isdir(root_location):
# 	root_list = os.listdir(root_location)
# 	for i in root_list:
# 		makeNode(root_location + "\\" + i)

makeNode(root_location)