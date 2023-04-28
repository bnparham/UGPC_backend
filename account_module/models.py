from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    uid = models.CharField(max_length=20, verbose_name="کد دانشجویی")
    email_activation_code = models.CharField(max_length=100, verbose_name="کد فعال سازی")
    is_capitan = models.BooleanField(verbose_name="شرکت به عنوان کاپیتان", default=False)
    has_team = models.BooleanField(verbose_name="تیم دارد/ندارد", default=False)

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        if self.first_name != "" and self.last_name != "" :
            return self.get_full_name()
        return self.email
