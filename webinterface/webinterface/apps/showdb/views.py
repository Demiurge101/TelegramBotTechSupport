from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import UploadFileForm
from .forms import AddDecimalNumber
from .forms import *
from uuid import uuid4

from .models import Stations
from .models import Devices
from .models import Clients
from .models import Users
from .models import DecimalNumbers
from .models import Files

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

def stations(request):
	if not request.user.is_authenticated:
		return index(request)
	stations = Stations.objects.all()
	return render(request, 'showdb/stations.html', {'stations': stations})

def devices(request):
	if not request.user.is_authenticated:
		return index(request)
	devices = Devices.objects.all()
	return render(request, 'showdb/devices.html', {'devices': devices})

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





def handle_uploaded_file(f):
	print(f"save file.")
	location = "C:/projects/garbage"
	uuid = uuid4()
	with open(f"{location}/{uuid}", "wb+") as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def upload_file(request):
	print(f"upload_file()")
	if request.method == "POST":
		file_form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES["file"])
			# return HttpResponseRedirect("/success/url/")
	else:
		file_form = UploadFileForm()
	return render(request, "showdb/edit_mkcb_form.html", {'file_form': file_form, 'decimal_obj': number, 'files':files})











def mkcb(request):
	if not request.user.is_authenticated:
		return index(request)
	mkcb = DecimalNumbers.objects.all()
	return render(request, 'showdb/mkcb.html', {'mkcb': mkcb})


def form_add_mkcb(request):
	if not request.user.is_authenticated:
		return index(request)
	form = AddDecimalNumber()
	return render(request, 'showdb/add_mkcb_form.html', {'form': form})

def edit_mkcb_form(request, decimal_number):
	print(f"edit_mkcb_form({decimal_number})")
	if not request.user.is_authenticated:
		return index(request)
	number = DecimalNumbers.objects.get(mkcb = decimal_number)
	files = Files.objects.filter(parent_number=decimal_number)
	file_form = UploadFileForm()
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
				m = DecimalNumbers.objects.create(mkcb=f"МКЦБ.{number}", field_name=name, location='uuid')
				m.save()
				print(f"after: {m}")
				return render(request, 'showdb/edit_mkcb_form.html', {'decimal_obj': m})
			else:
				print(f"Already exist!")
		return render(request, 'showdb/add_mkcb_form.html')
	except Exception as e:
		raise Http404(f"Error: Can't create DecimalNumber.\r\n {e}")


	return HttpResponseRedirect( reverse('showdb:mkcb'))

def edit_mkcb(request, decimal_number):
	if not request.user.is_authenticated:
		return index(request)

def delete_mkcb(request, decimal_number):
	DecimalNumbers.objects.filter(mkcb=decimal_number).delete()
	return HttpResponseRedirect( reverse('showdb:mkcb'))






