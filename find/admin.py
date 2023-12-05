from django.contrib import admin
from .models import FindPost, FindComment, FindReply

admin.site.register(FindPost)
admin.site.register(FindComment)
admin.site.register(FindReply)