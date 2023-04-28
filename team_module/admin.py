from django.contrib import admin

# Register your models here.
from .models import teamsModel,inviteModel

class teamAdmin(admin.ModelAdmin):
    list_display = ["teamName","capitan","teamMate1","teamMate2"]

class inviteAdmin(admin.ModelAdmin):
    list_display = ["sender", "reciver", "is_accept", "is_reject","invite_id"]

admin.site.register(teamsModel, teamAdmin)
admin.site.register(inviteModel, inviteAdmin)
