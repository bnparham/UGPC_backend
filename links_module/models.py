from django.db import models

# Create your models here.

class linksModel(models.Model):
    url_title = models.CharField(verbose_name="نام url", max_length=100)
    url_address = models.CharField(verbose_name="آدرس url", max_length=200)
    is_public = models.BooleanField(verbose_name="دسترسی عموم", default=True)
    is_active = models.BooleanField(verbose_name="برجسته شود/نشود", default=False)
    is_modal = models.BooleanField(verbose_name="نمایش به صورت مدال", default=False)
    modal_target_name = models.CharField(verbose_name="نام مدال", blank=True, null=True, max_length=100)
    is_show = models.BooleanField(verbose_name="نمایش داده شود/نشود", default=True)

    class Meta:
        verbose_name = "لینک"
        verbose_name_plural = "لینک ها"

    def __str__(self):
        return self.url_title