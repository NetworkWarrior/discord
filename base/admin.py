from django.contrib import admin
from .models import Group, Topic, Message, User
# Register your models here.

admin.site.register(Group)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)
