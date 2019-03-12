from django.contrib import admin
from .models import WikiModel, ItemModel, UserModel
# Register your models here.
admin.site.register(WikiModel)
admin.site.register(ItemModel)
admin.site.register(UserModel)
