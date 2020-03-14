from django import forms

from webapp.models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'name', 'file_status']

class FileNotStatusForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'name']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')