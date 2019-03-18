from django import forms
from .models import WikiModel, ItemModel, UserModel


class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords Must Match!")


class Wikiform(forms.ModelForm):
    class Meta:
        model = WikiModel
        labels = {'title': 'Title', 'textField': '', 'dateCreated': 'Date', 'imageUpload': 'Upload an Image'}

        exclude = ['foreignkeyToUserModel']



class ItemForm(forms.ModelForm):
    class Meta:
        model = ItemModel
        exclude = ['foreignkeyToWiki']


