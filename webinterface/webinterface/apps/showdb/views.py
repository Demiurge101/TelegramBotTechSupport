from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

import json

from uuid import uuid4
from datetime import datetime

from .forms import *
from .models import Stations
from .models import Devices
from .models import Clients
from .models import Users
from .models import DecimalNumbers
from .models import Files
from .models import Filebond

import Config

# Create your views here.


def check_user_access_to_group(request, target_group="editor"):
	if not request.user.is_authenticated:
		return False
	groups = request.user.groups.all()
	for group in groups:
		if str(group) == target_group:
			return True
	return False


def index(request):
	# data = Botool.objects.all()[:10]
	# data = {'one', 'two', 'three'}
	# stations = Stations.objects.all()
	# devices = Devices.objects.all()
	# orgs = Clients.objects.all()
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
	return render(request, 'showdb/auth.html', {"form": form})
	

def orgs(request):
	if not request.user.is_authenticated:
		return index(request)
	print(f"Authenticated: {request.user}")
	orgs = Clients.objects.all()
	techsupport = ''
	if check_user_access_to_group(request):
		techsupport = 'techsupport'

	return render(request, 'showdb/orgs.html', {'orgs': orgs, 'techsupport': techsupport})

def dates(request):
	if not request.user.is_authenticated:
		return index(request)
	pass




def auth(request):
	print("Request:")
	username = request.POST["login"]
	password = request.POST["password"]
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		orgs = Clients.objects.all()
		return HttpResponseRedirect( reverse('showdb:orgs'))
		# return render(request, 'showdb/orgs.html', {'orgs': orgs})
	else:
		return HttpResponseRedirect( reverse('showdb:index'))
		# return render(request, 'showdb/auth.html')

def log_out(request):
	logout(request)
	return HttpResponseRedirect( reverse('showdb:index'))
	# return render(request, 'showdb/auth.html')





def redirect_back(request, backlink="", number=""):
	if backlink == 'docs':
		return documents(request)
	elif backlink == 'device':
		return edit_device_form(request, number)
	elif backlink == 'mkcb':
		return edit_mkcb_form(request, number)
	elif backlink == 'station':
		return edit_station_form(request, number)
	return index(request)


def document_add_form(request, text=""):
	if not request.user.is_authenticated:
		return index(request)
	form = AddDocument()
	if request.method == 'POST':
		form = AddDocument(request.POST)
		if form.is_valid():
			print(f"form.cleaned_data: {form.cleaned_data}")
	return render(request, 'showdb/add_document_form.html', {'form': form, 'text': text})


def document_edit_form(request, uuid, backlink="docs", number="0"):
	if not request.user.is_authenticated:
		return index(request)
	form = AddDocument()
	if request.method == 'POST':
		form = AddDocument(request.POST)
		if form.is_valid():
			print(f"form.cleaned_data: {form.cleaned_data}")
			for i in form.cleaned_data:
				print(i)
	form.for_update(uuid)
	# if backlink:
	# 	return redirect_back(request, backlink, number)
	return render(request, 'showdb/add_document_form.html', {'form': form, 'backlink': backlink, 'number':number, 'uuid': uuid})

def documents(request, pos=0):
	step = 1000
	if not request.user.is_authenticated:
		return index(request)
	files = Files.objects.all()[pos*step:(pos+1)*step]
	count_files = Files.objects.count()
	if pos < 0:
		pos = 0
	if pos > count_files:
		pos = count_files
	pages = []
	k = 0
	while k * step < count_files:
		pages.append(k)
		k += 1
	techsupport = ''
	if check_user_access_to_group(request):
		techsupport = 'techsupport'
	return render(request, 'showdb/documents.html', {'techsupport':techsupport, 'files': files, 'pos':pos, 'pages': pages, 'count_files':count_files})

def save_uploaded_file(request, number = ""):
	if not request.user.is_authenticated:
		return index(request)
	print(f"save file.")
	location = Config.files_location
	uuid = uuid4()
	date = datetime.now().strftime("%Y-%m-%d")
	user_name = request.user.username
	frequest = request.FILES["file"]
	with open(f"{location}/{uuid}", "wb+") as destination:
		for chunk in frequest.chunks():
			destination.write(chunk)
	try:
		print(request.POST)
		file_name = request.POST['file_name']
		if not file_name:
			file_name = frequest
		file_obj = Files.objects.create(uuid=uuid, typef=request.POST['file_type'], namef=file_name, file_id=None, author=user_name, load_date=date)
		file_obj.save()
		if number:
			bond = Filebond.objects.create(snumber=number, uuid=uuid)
			bond.save()
	except Exception as e:
		print(e)

def upload_file(request, number="", backlink=""):
	print(f"upload_file({number}, {backlink})")
	if not request.user.is_authenticated:
		return index(request)
	if request.method == "POST":
		file_form = AddDocument(request.POST, request.FILES)
		if file_form.is_valid():
			save_uploaded_file(request, number)
	else:
		file_form = AddDocument()
	if backlink:
		return redirect_back(request, backlink, number)
	return render(request, 'showdb/add_document_form.html', {'form': file_form, 'number': number})

def update_file(request, uuid="", backlink="", number=""):
	print(f"UPDATE_FILE({uuid})")
	if not request.user.is_authenticated:
		return index(request)
	form = AddDocument()
	if request.method == 'POST':
		form = AddDocument(request.POST)
		if form.is_valid():
			print(f"form.cleaned_data: {form.cleaned_data}")
		# else:
		# 	print(form.non_field_errors)
		# 	for field in form.cleaned_data:
		# 		print(field)
		# 		print(form.cleaned_data[field])
		file_type = form.cleaned_data['file_type']
		file_name = form.cleaned_data['file_name']
		file = Files.objects.get(uuid=uuid)
		if file_type:
			file.file_type = file_type
		if file_name:
			file.namef = file_name
		file.save()
	else:
		print("NOT")
	form.for_update(uuid)
	if backlink:
		return redirect_back(request, backlink, number)
	return render(request, 'showdb/edit_document_form.html', {'form': form})


def bond_file(request, backlink="", number=""):
	if not request.user.is_authenticated:
		return index(request)
	form = SelectFileForm()
	if request.method == 'POST':
		form = SelectFileForm(request.POST)
		if form.is_valid():
			print(f"uuid: {form.cleaned_data['file']}")
			files = Filebond.objects.filter(snumber=number, uuid=form.cleaned_data['file'])
			print(f"Files: {files}")
			print(len(files))
			if len(files) == 0:
				fb = Filebond.objects.create(snumber=number, uuid=form.cleaned_data['file'])
				fb.save()
	if backlink:
		return redirect_back(request, backlink, number)
	return index(request)

def unbound_file(request, uuid, backlink="", number=""):
	if not request.user.is_authenticated:
		return index(request)
	print("Unbond file")
	Filebond.objects.filter(snumber=number, uuid=uuid).delete()
	return redirect_back(request, backlink, number)




def delete_file(request, uuid, backlink="", number=""):
	if not request.user.is_authenticated:
		return index(request)
	Files.objects.filter(uuid=uuid).delete()
	Filebond.objects.filter(uuid=uuid).delete()
	if backlink:
		return redirect_back(request, backlink, number)
	return HttpResponseRedirect( reverse('showdb:documents'))


def ajax_post_parser(request):
	pass

def ajax_filter_files(request):
	if not request.user.is_authenticated:
		return index(request)
	if request.method == 'POST':
		filter_text = request.POST.get('text')
		# filter_name = request.POST.get('name')
		# filter_type = request.POST.get('type')
		# filter_date = request.POST.get('date')
		files = {}
		if filter_text:
			if len(filter_text) < 4:
				filess = Files.objects.filter(typef=filter_text.lower())
			elif '-' in filter_text:
				filess = Files.objects.filter(load_date=filter_text)
			else:
				filess = Files.objects.filter(namef=filter_text) 
			print(f"Count: {filess.count()}")
			return HttpResponse(filess)
		return HttpResponse(json.dumps({'text': f"Another {filter_text}", 'files':files}), content_type="application/json")
	else :
		print("Stay out")
		return render_to_response('index.html', locals())







def mkcb(request):
	if not request.user.is_authenticated:
		return index(request)
	mkcb = DecimalNumbers.objects.all()
	techsupport = ''
	if check_user_access_to_group(request):
		techsupport = 'techsupport'
	return render(request, 'showdb/mkcb.html', {'mkcb': mkcb, 'techsupport': techsupport})


def form_add_mkcb(request, text=""):
	if not request.user.is_authenticated:
		return index(request)
	form = AddDecimalNumber()
	if request.method == 'POST':
		form = AddDecimalNumber(request.POST)
		if form.is_valid():
			print(f"form.cleaned_data: {form.cleaned_data}")
	return render(request, 'showdb/add_mkcb_form.html', {'form': form, 'text': text})

def edit_mkcb_form(request, decimal_number):
	print(f"edit_mkcb_form({decimal_number})")
	if not request.user.is_authenticated:
		return index(request)
	number = DecimalNumbers.objects.get(mkcb = decimal_number)
	bonds = Filebond.objects.filter(snumber=decimal_number)
	files = []
	print(f"Filebonds: \r\n{bonds}")
	for bond in bonds:
		file = Files.objects.get(uuid = bond)
		files.append(file)
		print(f"file: {file}")
	file_form = AddDocument()
	select_form = SelectFileForm()
	mkcb_form = EditDecimalNumber()
	mkcb_form.set_name(number.field_name)
	return render(request, 'showdb/edit_mkcb_form.html', {'mkcb_form': mkcb_form, 'file_form': file_form, 'select_form': select_form, 'decimal_obj': number, 'files':files})

def add_mkcb(request):
	if not request.user.is_authenticated:
		return index(request)
	print(f"add_mkcb()")
	try:
		number = request.POST['number']
		dot = number.find('.')
		dash = number.find('-')
		print(number)

		if dot == 6 and (len(number) == 10 and dash == -1 or len(number) == 13 and dash == 10):
			name = request.POST['name']
			print(f"Name: {name}")
			if not DecimalNumbers.objects.filter(mkcb=f"МКЦБ.{number}").exists():
				m = DecimalNumbers.objects.create(mkcb=f"МКЦБ.{number}", field_name=name)
				m.save()
				print(f"after: {m}")
				return render(request, 'showdb/edit_mkcb_form.html', {'decimal_obj': m})
			else:
				print(f"Already exist!")
				return form_add_mkcb(request, "Такой номер уже существует!")
			return render(request, 'showdb/auth.html', {"form": form})
		return render(request, 'showdb/add_mkcb_form.html')
	except Exception as e:
		raise Http404(f"Error: Can't create DecimalNumber.\r\n {e}")


	return HttpResponseRedirect( reverse('showdb:mkcb'))


def delete_mkcb(request, decimal_number):
	if not request.user.is_authenticated:
		return index(request)
	DecimalNumbers.objects.filter(mkcb=decimal_number).delete()
	return HttpResponseRedirect( reverse('showdb:mkcb'))


def update_mkcb(request, decimal_number):
	if not request.user.is_authenticated:
		return index(request)
	form = EditDecimalNumber()
	if request.method == 'POST':
		form = EditDecimalNumber(request.POST)
		if form.is_valid():
			print(f"form.cleaned_data: {form.cleaned_data}")
		mkcb_name = form.cleaned_data['field_name']
		decimal_obj = DecimalNumbers.objects.get(mkcb=decimal_number)
		if mkcb_name:
			decimal_obj.field_name = mkcb_name
		decimal_obj.save()
	return edit_mkcb_form(request, decimal_number)








def devices(request, pos=1):
	step = 500
	if not request.user.is_authenticated:
		return index(request)
	filter_form = DeviceFilterForm()
	devices = Devices.objects.all()
	pages = []
	count_devices = Devices.objects.count()
	if request.method == 'POST':
		filter_form = DeviceFilterForm(request.POST)
		if request.POST['date_out']:
			devices = devices.filter(date_out=request.POST['date_out'])
		if request.POST['org']:
			devices = devices.filter(org=request.POST['org'])
		if request.POST['mkcb']:
			devices = devices.filter(mkcb=request.POST['mkcb'])
		if request.POST['device_name']:
			devices = devices.filter(device_name=request.POST['device_name'])
	else:
		devices = devices[pos*step:(pos+1)*step]
		count_devices = Devices.objects.count()
		if pos < 0:
			pos = 0
		if pos > count_devices:
			pos = count_devices
		k = 0
		while k * step < count_devices:
			pages.append(k)
			k += 1
	count_devices = devices.count()
	techsupport = ''
	if check_user_access_to_group(request):
		techsupport = 'techsupport'
	return render(request, 'showdb/devices.html', {'devices': devices, 'filter_form': filter_form, 'count': count_devices, 'pos': pos, 'pages':pages, 'techsupport': techsupport})

def form_add_device(request, number=None):
	if not request.user.is_authenticated:
		return index(request)
	print(f"form_add_device({number})")
	form = AddDeviceForm()
	if number:
		form.set_station(number)
	if request.method == 'POST':
		form = AddDeviceForm(request.POST)
		if form.is_valid():
			device = form.save(commit=False)
			org = form.cleaned_data.get('station_number').org
			if org:
				print(f"ORG: {org}")
				device.org = org
			device.save()
			# form.save()
			print(f"form.cleaned_data: {form.cleaned_data}")
			return edit_device_form(request, form.cleaned_data['serial_number'])
	text = ''
	return render(request, 'showdb/add_device_form.html', {'form': form, 'text': text})


def add_device(request):
	if not request.user.is_authenticated:
		return index(request)
	number = request.POST['number']
	return edit_device_form(request, number)

def edit_device_form(request, number):
	if not request.user.is_authenticated:
		return index(request)
	device = Devices.objects.get(serial_number = number)
	bonds = Filebond.objects.filter(snumber=number)
	files = []
	print(f"Filebonds: \r\n{bonds}")
	for bond in bonds:
		file = Files.objects.get(uuid = bond)
		files.append(file)
		print(f"file: {file}")
	file_form = AddDocument()
	select_form = SelectFileForm()
	device_form = AddDeviceForm()
	device_form.set_device(device)
	return render(request, 'showdb/edit_device_form.html', {'device_form': device_form,'file_form': file_form, 'select_form': select_form, 'device': device, 'files':files})


def update_device(request, number):
	if not request.user.is_authenticated:
		return index(request)
	form = AddDeviceForm()
	if request.method == 'POST':
		form = AddDeviceForm(request.POST)
		if form.is_valid():
			print(f"form.cleaned_data: {form.cleaned_data}")
		device = Devices.objects.get(serial_number=number)
		if device:
			if form.cleaned_data['station_number']:
				device.station_number = form.cleaned_data['station_number']
			if form.cleaned_data['device_name']:
				device.device_name = form.cleaned_data['device_name']
			if form.cleaned_data['org']:
				device.org = form.cleaned_data['org']
			if form.cleaned_data['mkcb']:
				device.mkcb = form.cleaned_data['mkcb']
			if form.cleaned_data['date_out']:
				device.date_out = form.cleaned_data['date_out']
			if form.cleaned_data['description_field']:
				device.description_field = form.cleaned_data['description_field']
			device.save()
	return edit_device_form(request, number)


def delete_device(request, number):
	if not request.user.is_authenticated:
		return index(request)
	Devices.objects.filter(serial_number=number).delete()
	Filebond.objects.filter(snumber=number).delete()
	return HttpResponseRedirect( reverse('showdb:devices'))








def stations(request):
	if not request.user.is_authenticated:
		return index(request)
	filter_form = StationFilterForm()
	stations = Stations.objects.all()
	if request.method == 'POST':
		filter_form = StationFilterForm(request.POST)
		if request.POST['date_out']:
			stations = stations.filter(date_out=request.POST['date_out'])
		if request.POST['org']:
			stations = stations.filter(org=request.POST['org'])
		if request.POST['mkcb']:
			stations = stations.filter(mkcb=request.POST['mkcb'])
	techsupport = ''
	if check_user_access_to_group(request):
		techsupport = 'techsupport'
	return render(request, 'showdb/stations.html', {'stations': stations, 'filter_form' : filter_form, 'techsupport': techsupport})

def form_add_station(request):
	if not request.user.is_authenticated:
		return index(request)
	form = AddStationForm()
	if request.method == 'POST':
		form = AddStationForm(request.POST)
		if form.is_valid():
			form.save()
			print(f"form.cleaned_data: {form.cleaned_data}")
			return edit_station_form(request, form.cleaned_data['serial_number'])
	text = ''
	return render(request, 'showdb/add_station_form.html', {'form': form, 'text': text})


# def add_station(request):
# 	if not request.user.is_authenticated:
# 		return index(request)
# 	number = request.POST['serial_number']
# 	return edit_station_form(request, number)

def edit_station_form(request, number):
	if not request.user.is_authenticated:
		return index(request)
	station = Stations.objects.get(serial_number = number)
	devices = Devices.objects.filter(station_number = number)
	bonds = Filebond.objects.filter(snumber=number)
	files = []
	print(f"Filebonds: \r\n{bonds}")
	for bond in bonds:
		file = Files.objects.get(uuid = bond)
		files.append(file)
		print(f"file: {file}")
	file_form = AddDocument()
	select_form = SelectFileForm()
	station_form = AddStationForm()
	station_form.set_station(station)
	return render(request, 'showdb/edit_station_form.html', {'station_form': station_form,'file_form': file_form, 'select_form': select_form, 'station': station, 'devices': devices, 'files':files})


def update_station(request, number):
	if not request.user.is_authenticated:
		return index(request)
	form = AddStationForm()
	if request.method == 'POST':
		form = AddStationForm(request.POST)
		if form.is_valid():
			print(f"form.cleaned_data: {form.cleaned_data}")
		station = Stations.objects.get(serial_number=number)
		if station:
			if form.cleaned_data['org']:
				station.org = form.cleaned_data['org']
			if form.cleaned_data['mkcb']:
				station.mkcb = form.cleaned_data['mkcb']
			if form.cleaned_data['date_out']:
				station.date_out = form.cleaned_data['date_out']
			if form.cleaned_data['description_field']:
				station.description_field = form.cleaned_data['description_field']
			station.save()
	return edit_station_form(request, number)


def delete_station(request, number):
	if not request.user.is_authenticated:
		return index(request)
	Devices.objects.filter(station_number=number).delete()
	Stations.objects.filter(serial_number=number).delete()
	Filebond.objects.filter(snumber=number).delete()
	return HttpResponseRedirect( reverse('showdb:stations'))