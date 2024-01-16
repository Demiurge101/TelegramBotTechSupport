from django import forms
from .models  import *








class UploadFileForm(forms.Form):
    global decimal_file_types
    file = forms.FileField(label="Файл")




# class AddFileForm(forms.ModelForm):
#     class Meta:
#         model = Files
#         fields = ['typef']
#         widget = {
#             'typef': forms.ChoiceField(choices = decimal_file_types)
#         }

class AddDocument(forms.Form):
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




class AddTitleForm(forms.Form):
    title_name = forms.CharField(widget=forms.TextInput(attrs={'id':'title-name'}), max_length=65, label='Заголовок', required=True)
    command = forms.CharField(widget=forms.TextInput(attrs={'id':'command'}), max_length=65, label='Команда', required = False)
    content_text = forms.CharField(widget=forms.TextInput(attrs={'id':'content-text'}), max_length=65, label='Текст', required=True)


    def clean_command(self):
        cm = self.cleaned_data.get('command')
        if cm:
            if cm[0] != '/':
                return f"/{cm}"
        else:
            cm = None
        return cm

    def set_title(self, title):
        self.fields['title_name'].initial = title.title
        if title.title == '0_main':
            self.fields['title_name'].disabled = True
        self.fields['command'].initial = title.command
        self.fields['command'].required = False

    def set_content(self, content):
        self.fields['content_text'].initial = content.content_text
        self.fields['content_text'].required = False