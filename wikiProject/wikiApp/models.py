from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


class UserModel(models.Model):
    username = models.CharField(max_length=200, default="")
    password1 = models.CharField(max_length=200, default="")
    password2 = models.CharField(max_length=200, default="")
    dateAccountCreated = models.DateField(default=timezone.now)
    foreignkeyToUsers = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "Logged in as: " + str(self.username)


class WikiModel(models.Model):
    title = models.CharField(max_length=100)
    textField = models.TextField(max_length=1000)
    dateCreated = models.DateField(default=timezone.now)
    imageUpload = models.ImageField(upload_to="media", null=True, blank=True)
    foreignkeyToUserModel = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return f'/accounts/{self.id}'


class ItemModel(models.Model):
    itemField = models.CharField(max_length=100)
    imageUpload2 = models.CharField(max_length=200)
    foreignkeyToWiki = models.ForeignKey(WikiModel, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.itemField)
