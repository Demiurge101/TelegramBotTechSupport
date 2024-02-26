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
    file_type = forms.ChoiceField(label="Тип документа", choices = decimal_file_types, initial = ('и','Прочие инструкции (И)'))
    # self.fields['file_type'].initial = ('и','Прочие инструкции (И)')
    file = forms.FileField(label="Файл", widget = forms.ClearableFileInput(attrs={'id':'select-file'}), )
    file_name = forms.CharField(widget=forms.TextInput(attrs={'id':'name-selected-file'}), label="Имя файла", max_length=255, required=False)

    def for_update(self, uuid):
        print(f"for_update({uuid})")
        # for f in self.fields:
        #     print(f)
        #     print(self.fields[f])
        file_obj = Files.objects.get(uuid =  uuid)
        # for tp in decimal_file_types:
        #     print(tp)
        # print(decimal_file_types[0])
        self.fields['file'].widget = forms.HiddenInput()
        self.fields['file'].label = ""
        self.fields['file'].required = False
        self.fields['file'].disabled = True
        file_type = file_obj.typef
        initial_file_type = ('и','Прочие инструкции (И)')
        for t in decimal_file_types:
            if file_type == t[0]:
                initial_file_type = t
        for t in serial_file_types:
            if file_type == t[0]:
                initial_file_type = t
        self.fields['file_type'].initial = initial_file_type
        self.fields['file_name'].initial = file_obj.namef

        # self.initial['file_type'] = decimal_file_types[2]
        # file_type.initial = 'default value'
        # file.required = False


class AddDecimalNumber(forms.Form):
    number = forms.CharField(label="Децимальный номер", max_length=25)
    name = forms.CharField(label="Название", max_length=255)

class EditDecimalNumber(forms.Form):
    field_name = forms.CharField(label="Название", max_length=255)

    def set_name(self, current_name):
        # print(f"set_name({current_name})")
        # for field in self.fields:
        #     print(field)
        self.fields['field_name'].initial = current_name


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
        self.fields['serial_number'] = forms.CharField(min_length=4, max_length=8, label='Серийный номер')
        # self.fields['serial_number'].max_length = 8
        # self.fields['serial_number'].min_length = 4
        self.fields['mkcb'] = forms.ModelChoiceField(to_field_name='mkcb', label='МКЦБ', queryset=DecimalNumbers.objects.all(), empty_label='Не выбрано')
        self.fields['date_out'].required = True
        self.fields['org'].empty_label = "Не выбрано"
        # self.fields['org'].attrs = {'class':'form-common'}

    class Meta:
        model = Stations
        fields = ['serial_number', 'org', 'mkcb', 'date_out', 'description_field']

    def clean_mkcb(self):
        return self.cleaned_data.get('mkcb').mkcb

    def test(self):
        self.fields['serial_number'] = None

    def set_station(self, station):
        self.fields['serial_number'].initial = station.serial_number
        self.fields['serial_number'].disabled = True
        self.fields['org'].initial = station.org
        self.fields['mkcb'].initial = station.mkcb
        self.fields['date_out'].initial = station.date_out
        self.fields['description_field'].initial = station.description_field

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
        self.fields['serial_number'] = forms.CharField(min_length=4, max_length=8, label='Серийный номер')
        self.fields['station_number'] = forms.ModelChoiceField(to_field_name='serial_number', queryset=Stations.objects.all(), empty_label='Не выбрано', widget=forms.Select(attrs={'id':'station-field'}), label='Станция')
        self.fields['station_number'].required = False
        # self.fields['serial_number'].max_length = 8
        # self.fields['serial_number'].min_length = 4
        self.fields['mkcb'] = forms.ModelChoiceField(to_field_name="mkcb", queryset=DecimalNumbers.objects.all(), empty_label='Не выбрано', label='МКЦБ')
        self.fields['date_out'].required = True
        self.fields['org'] = forms.ModelChoiceField(to_field_name='org', label='Организация', queryset=Clients.objects.all(), widget = forms.Select(attrs={'id':'org-field'}), empty_label='Не выбрано')
        # self.fields['org'].widget = forms.Select(attrs={'id':'org-field'})
        self.fields['org'].empty_label = "Не выбрано"

    class Meta:
        model = Devices
        fields = ['serial_number', 'station_number', 'device_name', 'org', 'mkcb', 'date_out', 'description_field']

    def clean_mkcb(self):
        return self.cleaned_data.get('mkcb').mkcb

    def set_station(self, number):
        self.fields['station_number'] = forms.ModelChoiceField(to_field_name='serial_number', queryset=Stations.objects.filter(serial_number=number), empty_label=None)
        self.fields['org'].empty_label = None
        org = Stations.objects.get(serial_number=number).org
        print(f"ORG: {org}")
        self.fields['org'].queryset = Clients.objects.filter(org=org)
        # self.fields['org'].disabled = True


    def set_device(self, device):
        self.fields['serial_number'].initial = device.serial_number
        self.fields['serial_number'].disabled = True
        self.fields['station_number'].initial = device.station_number
        if device.station_number:
            self.fields['org'].disabled = True
        self.fields['org'].initial = device.org
        self.fields['device_name'].initial = device.device_name
        self.fields['mkcb'].initial = device.mkcb
        self.fields['date_out'].initial = device.date_out
        self.fields['description_field'].initial = device.description_field



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
        self.fields['serial_number'].required = False

    class Meta:
        model = Stations
        fields = ['org', 'mkcb', 'date_out', 'serial_number']
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
        self.fields['serial_number'].required = False

    class Meta:
        model = Devices
        fields = ['org', 'mkcb', 'date_out', 'device_name', 'serial_number']
        # widgets = {
        #     'mkcb' : forms.ModelChoiceField(queryset=DecimalNumbers.objects.all())
        # }


class SelectFileForm(forms.Form):
    file = forms.ModelChoiceField(queryset=Files.objects.all(), empty_label=None, label="Файл", widget=forms.Select(attrs={'id':'filter-input'}))
    def clean_file(self):
        return self.cleaned_data.get('file').uuid