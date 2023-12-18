from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

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
	return render(request, 'showdb/orgs.html', {'orgs': orgs})

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






def document_add_form(request, text=""):
	if not request.user.is_authenticated:
		return index(request)
	form = AddDocument()
	if request.method == 'POST':
		form = AddDocument(request.POST)
		if form.is_valid():
			print(f"form.cleaned_data: {form.cleaned_data}")
	return render(request, 'showdb/add_document_form.html', {'form': form, 'text': text})


def document_edit_form(request, uuid):
	if not request.user.is_authenticated:
		return index(request)
	files = Files.objects.all()
	return render(request, 'showdb/documents.html', {'files': files})

def documents(request):
	if not request.user.is_authenticated:
		return index(request)
	files = Files.objects.all()
	return render(request, 'showdb/documents.html', {'files': files})

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

def upload_file(request, number=""):
	print(f"upload_file({number})")
	if not request.user.is_authenticated:
		return index(request)
	if request.method == "POST":
		file_form = AddDocument(request.POST, request.FILES)
		if file_form.is_valid():
			save_uploaded_file(request, number)
	else:
		file_form = AddDocument()
	if number:
		if number[:4] == 'МКЦБ':
			return edit_mkcb_form(request, number)
	return render(request, 'showdb/add_document_form.html', {'form': file_form, 'number': number})


def delete_file(request, uuid):
	if not request.user.is_authenticated:
		return index(request)
	Files.objects.filter(uuid=uuid).delete()
	Filebond.objects.filter(uuid=uuid).delete()
	return HttpResponseRedirect( reverse('showdb:documents'))










def mkcb(request):
	if not request.user.is_authenticated:
		return index(request)
	mkcb = DecimalNumbers.objects.all()
	return render(request, 'showdb/mkcb.html', {'mkcb': mkcb})


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
	return render(request, 'showdb/edit_mkcb_form.html', {'file_form': file_form, 'decimal_obj': number, 'files':files})

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

def edit_mkcb(request, decimal_number):
	if not request.user.is_authenticated:
		return index(request)

def delete_mkcb(request, decimal_number):
	if not request.user.is_authenticated:
		return index(request)
	DecimalNumbers.objects.filter(mkcb=decimal_number).delete()
	return HttpResponseRedirect( reverse('showdb:mkcb'))








def devices(request):
	if not request.user.is_authenticated:
		return index(request)
	filter_form = DeviceFilterForm()
	devices = Devices.objects.all()
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
	return render(request, 'showdb/devices.html', {'devices': devices, 'filter_form': filter_form})

def form_add_device(request):
	if not request.user.is_authenticated:
		return index(request)
	form = AddDeviceForm()
	if request.method == 'POST':
		form = AddDeviceForm(request.POST)
		if form.is_valid():
			# device = form.save(commit=False)
			# device.mkcb = form.cleaned_data.get('mkcb').mkcb
			# device.station_number = form.cleaned_data.get('station_number').serial_number
			# device.save()
			form.save()
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
	return render(request, 'showdb/edit_device_form.html', {'file_form': file_form, 'device': device, 'files':files})


def edit_device(request):
	if not request.user.is_authenticated:
		return index(request)

def delete_device(request, number):
	if not request.user.is_authenticated:
		return index(request)
	Devices.objects.filter(serial_number=number).delete()
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
	
	return render(request, 'showdb/stations.html', {'stations': stations, 'filter_form' : filter_form})

def form_add_station(request):
	if not request.user.is_authenticated:
		return index(request)
	form = AddStationForm()
	if request.method == 'POST':
		form = AddStationForm(request.POST)
		if form.is_valid():
			# station = form.save(commit=False)
			# station.mkcb = form.cleaned_data.get('mkcb').mkcb
			# station.save()
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
	return render(request, 'showdb/edit_station_form.html', {'file_form': file_form, 'station': station, 'devices': devices, 'files':files})


def edit_station(request):
	if not request.user.is_authenticated:
		return index(request)

def delete_station(request, number):
	if not request.user.is_authenticated:
		return index(request)
	Devices.objects.filter(station_number=number).delete()
	Stations.objects.filter(serial_number=number).delete()
	return HttpResponseRedirect( reverse('showdb:stations'))