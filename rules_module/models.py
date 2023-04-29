from django.db import models

# Create your models here.
class rulesModel(models.Model):
    title = models.CharField(max_length=100,verbose_name="نام قانون")
    description = models.CharField(max_length=300, verbose_name="توضیخ")
    is_show = models.BooleanField(default=True, verbose_name="نمایش داده شود / نشود")