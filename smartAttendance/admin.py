from django.contrib import admin
from .models import User, Attendance, Message

admin.site.register(User)
admin.site.register(Attendance)
admin.site.register(Message)
