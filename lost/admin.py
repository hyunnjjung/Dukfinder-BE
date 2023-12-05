from django.contrib import admin
from .models import LostPost, Comment, Reply

admin.site.register(LostPost)
admin.site.register(Comment)
admin.site.register(Reply)