from django import forms
from .models  import *








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



class LoginForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'id':'login', 'class':'login'}), max_length=65, label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'password'}), label="Пароль")



class SelectFileForm(forms.Form):
    file = forms.ModelChoiceField(queryset=Files.objects.all(), empty_label=None, label="Файл", widget=forms.Select(attrs={'id':'filter-input'}))
    def clean_file(self):
        return self.cleaned_data.get('file').uuid