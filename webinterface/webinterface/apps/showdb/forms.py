from django import forms
from .models  import *

decimal_file_types = [('сб','Сборочный чертёж (СБ)'), 
('сп','Спецификация (СП)'), 
('э','Схемы электрические (Э)'), 
('fw','Прошивка и инструкция по прошивке (FW)'), 
('рэ','Руководство по эксплуатации (РЭ)'), 
('сэр','Сертификаты и свидетельства (СЕР)'), 
('по','Программное обеспечение (ПО)'), 
('и','Прочие инструкции (И)')
]
serial_file_types = [
('пс','Паспорт (ПС)'),
('ао','Акт опрессовки (АО)'),
('пк','Протокол калибровки (ПК)'),
('пп','Протокол поверки (ПП)')
]


class UploadFileForm(forms.Form):
    global decimal_file_types
    file_type = forms.ChoiceField(label="Тип файла", choices = decimal_file_types)
    file = forms.FileField(label="Файл")




# class AddFileForm(forms.ModelForm):
#     class Meta:
#         model = Files
#         fields = ['typef']
#         widget = {
#             'typef': forms.ChoiceField(choices = decimal_file_types)
#         }

class AddDocument(forms.Form):
    global decimal_file_types
    file_type = forms.ChoiceField(label="Тип документа", choices = decimal_file_types)
    file = forms.FileField(label="Файл", )
    file_name = forms.CharField(label="Новое имя файла", max_length=255, required=False)


class AddDecimalNumber(forms.Form):
    number = forms.CharField(label="Децимальный номер", max_length=25)
    name = forms.CharField(label="Название", max_length=255)


class AddStationForm(forms.Form):
    number = forms.CharField(label="Номер", min_length=8, max_length=8)
    org = forms.ModelChoiceField(label="Организация", queryset=Clients.objects.all())
    mkcb = forms.ModelChoiceField(label="Децимальный номер", queryset=DecimalNumbers.objects.all())
    date = forms.DateField(label="Дата отправки", input_formats="%Y-%m-%d")
    description = forms.CharField(label="Примечание", max_length=255, required=False)


class AddDeviceForm(forms.Form):
    number = forms.CharField(label="Номер", min_length=8, max_length=8)
    device_name = forms.CharField(label="Название", max_length=255)
    station_number = forms.ModelChoiceField(label="Номер станции (не обязательно)", queryset=Stations.objects.all(), required=False)
    org = forms.ModelChoiceField(label="Организация", queryset=Clients.objects.all())
    mkcb = forms.ModelChoiceField(label="Децимальный номер", queryset=DecimalNumbers.objects.all())
    date = forms.DateField(label="Дата отправки", input_formats="%Y-%m-%d")
    description = forms.CharField(label="Примечание", max_length=255, required=False)



class LoginForm(forms.Form):
    login = forms.CharField(max_length=65, label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")