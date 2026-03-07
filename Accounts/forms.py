from django import forms
from .models import Register_master
class registerform(forms.ModelForm):
    class Meta:
        model=Register_master
        fields="__all__"

class loginform(forms.ModelForm):
    class Meta:
        model=Register_master
        fields=['email','password']