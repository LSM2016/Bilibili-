from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('oid', 'rpid', 'mid', 'username', 'ctime', 'content')
    search_fields = ('oid', 'mid')
