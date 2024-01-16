from django.shortcuts import render

# Create your views here.
from .models import *
from .forms import *

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

import json

from uuid import uuid4
from datetime import datetime

import Config

def index(request):
	if not request.user.is_authenticated:
		form = LoginForm()
		if request.method == 'POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				print(form.cleaned_data)
		return render(request, 'showdb/auth.html', {"form": form})
	# data = Botool.objects.all()[:10]
	# data = {'one', 'two', 'three'}
	titles = Titles.objects.all()
	# devices = Devices.objects.all()
	# orgs = Clients.objects.all()
	return render(request, 'tseditor/titles.html', {'titles': titles})


def title(request, titleid=0):
	if not request.user.is_authenticated:
		return index(request)
	# if titleid<1:
	# 	return index(request)
	print(":", titleid)
	title = None
	content = None
	file_form = AddDocument()
	select_form = SelectFileForm()
	title_form = AddTitleForm()
	if titleid > 0:
		title = Titles.objects.get(title_id = titleid)
		content = Contents.objects.get(parent_id = titleid)
		if title:
			title_form.set_title(title)
		if content:
			title_form.set_content(content)
		bonds = Filebond.objects.filter(title_id=titleid)
		files = []
		print(f"Filebonds: \r\n{bonds}")
		for bond in bonds:
			file = Files.objects.get(uuid = bond)
			files.append(file)
	subtitles = Titles.objects.filter(parent_id = titleid)
	return render(request, 'tseditor/title.html', {'title': title, 'content':content, 'title_form': title_form,'subtitles': subtitles, 'file_form': file_form, 'select_form': select_form, 'files':files})

# def form_add_title(request, parentid=0):
# 	if not request.user.is_authenticated:
# 		return index(request)
# 	title_form = AddTitleForm()
# 	return render(request, 'tseditor/add_title_form.html', {'form': title_form, 'title_id': parentid})

def add_title(request, parentid=0):
	if not request.user.is_authenticated:
		return index(request)
	if request.method == 'POST':
		form = AddTitleForm(request.POST)
		if form.is_valid():
			title_name = form.cleaned_data['title_name']
			command = form.cleaned_data['command']
			content_text = form.cleaned_data['content_text']
			if title_name:
				if command:
					if Titles.objects.filter(command=command):
						command=None
						print('This command already exist!')
				title_obj = Titles.objects.create(parent_id=parentid, title=title_name, command=command, title_type=1)
				title_obj.save()
				print(title_obj.title_id)
				content = Contents.objects.create(parent=title_obj, content_text=content_text)
				return title(request, title_obj.title_id)
		return title(request, parentid)
	else:
		title_form = AddTitleForm()
		return render(request, 'tseditor/add_title_form.html', {'form': title_form, 'title_id': parentid})



def update_title(request, titleid):
	if not request.user.is_authenticated:
		return index(request)
	if request.method == 'POST':
		form = AddTitleForm(request.POST)
		if form.is_valid():
			title_obj = Titles.objects.get(title_id=titleid)
			title_name = form.cleaned_data['title_name']
			command = form.cleaned_data['command']
			content_text = form.cleaned_data['content_text']
			if title_name:
				title_obj.title = title_name
			if command:
				print(f'command: <{command}>')
				title_obj.command = command
			else:
				title_obj.command = None
			title_obj.save()
			if content_text:
				content = Contents.objects.get(parent=title_obj)
				content.content_text = content_text
				content.save()
			return title(request, title_obj.title_id)
		return title(request, parentid)
	else:
		title_form = AddTitleForm()
		return render(request, 'tseditor/add_title_form.html', {'form': title_form, 'title_id': parentid})


def delete_title(request, titleid=0):
	if not request.user.is_authenticated:
		return index(request)
	if titleid > 0:
		title_obj = Titles.objects.get(title_id=titleid)
		parentid = title_obj.parent_id
		Filebond.objects.filter(title_id=titleid).delete()
		Contents.objects.filter(parent=title_obj).delete()
		subtitles = Titles.objects.filter(parent_id=titleid)
		for subtitle in subtitles:
			delete_title(request, subtitle.title_id)
		Titles.objects.filter(title_id=titleid).delete()
		return title(request, parentid)
	return title(request, titleid)













def document_edit_form(request, titleid, uuid):
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
	return render(request, 'tseditor/add_document_form.html', {'form': form, 'titleid':titleid, 'uuid': uuid})


def save_uploaded_file(request,  titleid=0):
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
		file_obj = Files.objects.create(uuid=uuid, namef=file_name, file_id=None, author=user_name, load_date=date)
		file_obj.save()
		if titleid > 0:
			bond = Filebond.objects.create(title_id=titleid, uuid=uuid)
			bond.save()
	except Exception as e:
		print(e)

def upload_file(request, titleid=0):
	print(f"upload_file({titleid})")
	if not request.user.is_authenticated:
		return index(request)
	if request.method == "POST":
		file_form = AddDocument(request.POST, request.FILES)
		if file_form.is_valid():
			save_uploaded_file(request, titleid)
	else:
		file_form = AddDocument()
	return title(request, titleid)

def update_file(request, titleid=0, uuid=""):
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
		file_name = form.cleaned_data['file_name']
		file = Files.objects.get(uuid=uuid)
		if file_name:
			file.namef = file_name
		file.save()
	else:
		print("NOT")
	form.for_update(uuid)
	return title(request, titleid)


def bond_file(request, titleid=0):
	print("Bond file")
	form = SelectFileForm()
	if request.method == 'POST':
		form = SelectFileForm(request.POST)
		if form.is_valid():
			print(f"uuid: {form.cleaned_data['file']}")
			files = Filebond.objects.filter(title_id=titleid, uuid=form.cleaned_data['file'])
			print(f"Files: {files}")
			print(len(files))
			if len(files) == 0:
				fb = Filebond.objects.create(title_id=titleid, uuid=form.cleaned_data['file'])
				fb.save()
	return title(request, titleid)

def unbound_file(request, titleid, uuid):
	if not request.user.is_authenticated:
		return index(request)
	print("Unbond file")
	Filebond.objects.filter(title_id=titleid, uuid=uuid).delete()
	return title(request, titleid)




def delete_file(request, uuid, titleid=0):
	if not request.user.is_authenticated:
		return index(request)
	Filebond.objects.filter(uuid=uuid).delete()
	Files.objects.filter(uuid=uuid).delete()
	return title(request, titleid)