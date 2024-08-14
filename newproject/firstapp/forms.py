from django import forms
from .models import sampleforms

# class sampleforms(forms.Form):
#     rollno=forms.IntegerField()
#     name=forms.CharField(max_length=50)
#     age=forms.IntegerField()

class modelform(forms.ModelForm):
    class Meta:
        model=sampleforms
        #fields='__all__'
        fields=['name','rollno']
