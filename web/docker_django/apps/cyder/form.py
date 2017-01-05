from django import forms
from .models import UserModel


class UserModelDescriptionForm(forms.ModelForm):

    class Meta:
        model = UserModel
        fields = ('name', 'description',)
