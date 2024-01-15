from django.shortcuts import render

# Create your views here.
from .models import Titles
from .models import Contents

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

def index(request):
	# data = Botool.objects.all()[:10]
	# data = {'one', 'two', 'three'}
	titles = Titles.objects.all()
	# devices = Devices.objects.all()
	# orgs = Clients.objects.all()
	return render(request, 'tseditor/titles.html', {'titles': titles})


def title(request, title_id):
	titles = Titles.objects.filter(parent_id = title_id)
	return render(request, 'tseditor/titles.html', {'titles': titles})