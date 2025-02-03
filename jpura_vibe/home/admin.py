from django.contrib import admin
from . models import Rooms, Topic, Message, Profile

admin.site.register(Rooms)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Profile)