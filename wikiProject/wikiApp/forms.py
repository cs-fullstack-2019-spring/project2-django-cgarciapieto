from django import forms
from .models import WikiModel, ItemModel, UserModel


class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password1', 'password2']


class Wikiform(forms.ModelForm):
    class Meta:
        model = WikiModel

        fields = '__all__'


class ItemForm(forms.ModelForm):
    class Meta:
        model = ItemModel
        fields = '__all__'
