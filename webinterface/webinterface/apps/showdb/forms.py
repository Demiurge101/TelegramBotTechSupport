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
    file_type = forms.ChoiceField(choices = decimal_file_types)
    file = forms.FileField()




# class AddFileForm(forms.ModelForm):
#     class Meta:
#         model = Files
#         fields = ['typef']
#         widget = {
#             'typef': forms.ChoiceField(choices = decimal_file_types)
#         }

class AddDocument(forms.Form):
    global decimal_file_types
    file_type = forms.ChoiceField(choices = decimal_file_types)
    file = forms.FileField()
    file_name = forms.CharField(max_length=255, required=False)


class AddDecimalNumber(forms.Form):
    number = forms.CharField(max_length=25)
    name = forms.CharField(max_length=255)


class LoginForm(forms.Form):
    login = forms.CharField(max_length=65, label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")