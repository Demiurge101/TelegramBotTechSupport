from django.shortcuts import render

# Create your views here.
from .models import *
from .forms import *

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

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
	subtitles = Titles.objects.filter(parent_id = titleid)
	return render(request, 'tseditor/title.html', {'title': title, 'content':content, 'title_form': title_form,'subtitles': subtitles, 'file_form': file_form, 'select_form': select_form,})

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