from django.contrib import admin
from .models import *
# Register your models here.

class rulesAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "is_show"]
    list_editable = ["is_show"]

admin.site.register(rulesModel, rulesAdmin)