from django import forms
import os

#拡張子をcsvのみにする
VALID_EXTENSIONS = ['.csv']

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=200)
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data['file']
        extension = os.path.splitext(file.name)[1] #拡張子を取得
        if not extension.lower() in VALID_EXTENSIONS:
            raise forms.ValidationError('csv only!')