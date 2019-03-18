from django import forms
from .models import WikiModel, ItemModel, UserModel

# pulls in Models and uses the fields to create a form that user can input required data into

class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password1', 'password2']
    # this validation is done so the passwords must match, if the passwords dont != match a validation error is raised
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords Must Match!")

# forms for  posts
class Wikiform(forms.ModelForm):
    class Meta:
        model = WikiModel
        # created personalized labels
        labels = {'title': 'Title', 'textField': '', 'dateCreated': 'Date', 'imageUpload': 'Upload an Image'}

        exclude = ['foreignkeyToUserModel']
# form fo items


class ItemForm(forms.ModelForm):
    class Meta:
        model = ItemModel
        exclude = ['foreignkeyToWiki']


