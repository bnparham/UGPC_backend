from django.contrib import admin
from .models import  linksModel
# Register your models here.

class linksModel_admin(admin.ModelAdmin):
    list_display = ["url_title", "url_address", "is_public", "is_active", "is_modal", "modal_target_name"]

admin.site.register(linksModel, linksModel_admin)