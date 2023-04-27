from django.contrib import admin

# Register your models here.
from .models import teamsModel

class teamAdmin(admin.ModelAdmin):
    list_display = ["teamName","capitan","teamMate1","teamMate2"]

admin.site.register(teamsModel, teamAdmin)