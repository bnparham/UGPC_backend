from django.contrib import admin
from .models import User

# Register your models here.

class user_panel(admin.ModelAdmin):
    list_display = ["email", "is_active", "last_login", "is_capitan", "has_team"]

admin.site.register(User, user_panel)