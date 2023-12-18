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


# class AddStationForm(forms.Form):
#     number = forms.CharField(label="Номер", min_length=8, max_length=8)
#     org = forms.ModelChoiceField(label="Организация", queryset=Clients.objects.all())
#     mkcb = forms.ModelChoiceField(label="Децимальный номер", queryset=DecimalNumbers.objects.all())
#     date = forms.DateField(label="Дата отправки", input_formats="%Y-%m-%d")
#     description = forms.CharField(label="Примечание", max_length=255, required=False)


class AddStationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_out'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['serial_number'] = forms.CharField(min_length=4, max_length=8)
        # self.fields['serial_number'].max_length = 8
        # self.fields['serial_number'].min_length = 4
        self.fields['mkcb'] = forms.ModelChoiceField(to_field_name='mkcb', queryset=DecimalNumbers.objects.all(), empty_label='Не выбрано')
        self.fields['date_out'].required = True

    class Meta:
        model = Stations
        fields = ['serial_number', 'org', 'mkcb', 'date_out', 'description_field']

    def clean_mkcb(self):
        return self.cleaned_data.get('mkcb').mkcb

    # def clean_org(self):
    #     return self.cleaned_data.get('org').org
        # if len(mkcb) > 25:
        #     print(forms.ValidationError("mkcb must to contain 9 digits."))
            # return self.cleaned_data   # <--- DON'T DO THIS
        # return mkcb['mkcb']




# class AddDeviceForm(forms.Form):
#     number = forms.CharField(label="Номер", min_length=8, max_length=8)
#     device_name = forms.CharField(label="Название", max_length=255)
#     station_number = forms.ModelChoiceField(label="Номер станции (не обязательно)", queryset=Stations.objects.all(), required=False)
#     org = forms.ModelChoiceField(label="Организация", queryset=Clients.objects.all())
#     mkcb = forms.ModelChoiceField(label="Децимальный номер", queryset=DecimalNumbers.objects.all())
#     date = forms.DateField(label="Дата отправки", input_formats="%Y-%m-%d")
#     description = forms.CharField(label="Примечание", max_length=255, required=False)

class AddDeviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_out'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['serial_number'] = forms.CharField(min_length=4, max_length=8)
        self.fields['station_number'] = forms.ModelChoiceField(to_field_name='serial_number', queryset=Stations.objects.all(), empty_label='Не выбрано')
        self.fields['station_number'].required = False
        # self.fields['serial_number'].max_length = 8
        # self.fields['serial_number'].min_length = 4
        self.fields['mkcb'] = forms.ModelChoiceField(to_field_name="mkcb", queryset=DecimalNumbers.objects.all(), empty_label='Не выбрано')
        self.fields['date_out'].required = True

    class Meta:
        model = Devices
        fields = ['serial_number', 'station_number', 'device_name', 'org', 'mkcb', 'date_out', 'description_field']

    def clean_mkcb(self):
        return self.cleaned_data.get('mkcb').mkcb

    # def clean_org(self):
    #     return self.cleaned_data.get('org').org

    # def clean_station_number(self):
    #     print('clean_data()')
    #     print(self.cleaned_data.get('station_number').serial_number)
    #     return self.cleaned_data.get('station_number').serial_number


class LoginForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'id':'login', 'class':'login'}), max_length=65, label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'password'}), label="Пароль")



# class FilterForm(forms.Form):
#     date = forms.DateField(label="Дата отправки")

class StationFilterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_out'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )

        self.fields['mkcb'] = forms.ModelChoiceField(queryset=DecimalNumbers.objects.all())
        self.fields['mkcb'].required = False
        self.fields['mkcb'].empty_label = 'Все'
        self.fields['mkcb'].max_length = 255
        self.fields['org'].empty_label = 'Все'
        self.fields['org'].required = False
        self.fields['date_out'].required = False

    class Meta:
        model = Stations
        fields = ['org', 'mkcb', 'date_out']
        # widgets = {
        #     'mkcb' : forms.ModelChoiceField(queryset=DecimalNumbers.objects.all())
        # }


class DeviceFilterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_out'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )

        self.fields['mkcb'] = forms.ModelChoiceField(queryset=DecimalNumbers.objects.all())
        self.fields['mkcb'].required = False
        self.fields['mkcb'].empty_label = 'Все'
        self.fields['mkcb'].max_length = 255
        self.fields['org'].empty_label = 'Все'
        self.fields['org'].required = False
        self.fields['date_out'].required = False
        self.fields['device_name'].required = False

    class Meta:
        model = Devices
        fields = ['org', 'mkcb', 'date_out', 'device_name']
        # widgets = {
        #     'mkcb' : forms.ModelChoiceField(queryset=DecimalNumbers.objects.all())
        # }