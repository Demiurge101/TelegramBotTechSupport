from django.shortcuts import render

import uuid
# Create your views here.

from .models import Stations
from .models import Devices
from .models import Clients
from .models import Users
from .models import DecimalNumbers

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

def index(request):
	# data = Botool.objects.all()[:10]
	# data = {'one', 'two', 'three'}
	# stations = Stations.objects.all()
	# devices = Devices.objects.all()
	# orgs = Clients.objects.all()
	return render(request, 'showdb/auth.html')
	

def orgs(request):
	if not request.user.is_authenticated:
		return render(request, 'showdb/auth.html')
	print(f"Authenticated: {request.user}")
	orgs = Clients.objects.all()
	return render(request, 'showdb/orgs.html', {'orgs': orgs})

def dates(request):
	if not request.user.is_authenticated:
		return render(request, 'showdb/auth.html')
	pass

def stations(request):
	if not request.user.is_authenticated:
		return render(request, 'showdb/auth.html')
	stations = Stations.objects.all()
	return render(request, 'showdb/stations.html', {'stations': stations})

def devices(request):
	if not request.user.is_authenticated:
		return render(request, 'showdb/auth.html')
	devices = Devices.objects.all()
	return render(request, 'showdb/devices.html', {'devices': devices})

def auth(request):
	print("Request:")
	# print(request.session)
	# for i in request.session:
	# 	print(i)
	username = request.POST["login"]
	password = request.POST["pass"]
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







def mkcb(request):
	if not request.user.is_authenticated:
		return render(request, 'showdb/auth.html')
	mkcb = DecimalNumbers.objects.all()
	return render(request, 'showdb/mkcb.html', {'mkcb': mkcb})


def form_add_mkcb(request):
	if not request.user.is_authenticated:
		return render(request, 'showdb/auth.html')
	return render(request, 'showdb/add_mkcb_form.html')
def edit_mkcb_form(request, decimal_number):
	if not request.user.is_authenticated:
		return render(request, 'showdb/auth.html')
	number = DecimalNumbers.objects.get(mkcb = decimal_number)
	return render(request, 'showdb/edit_mkcb_form.html', {'decimal_obj': number})

def add_mkcb(request):
	if not request.user.is_authenticated:
		return render(request, 'showdb/auth.html')
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
		return render(request, 'showdb/auth.html')

def delete_mkcb(request, decimal_number):
	DecimalNumbers.objects.filter(mkcb=decimal_number).delete()
	return HttpResponseRedirect( reverse('showdb:mkcb'))






