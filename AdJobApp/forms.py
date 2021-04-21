from django import forms

class UpoadFileForm(forms.Form):
    title = forms.CharField(max_length=200)
    file = forms.FileField()