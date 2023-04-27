from django.db import models
from account_module.models import User

# Create your models here.
class teamsModel(models.Model):
    teamName = models.CharField(verbose_name="نام تیم", max_length=200)
    capitan = models.ForeignKey(User, verbose_name="کاپیتان", on_delete=models.CASCADE, related_name="captian")
    teamMate1 = models.OneToOneField(User, verbose_name="هم تیمی اول", on_delete=models.CASCADE, related_name="firstTeamMate", default=None, null=True)
    teamMate2 = models.OneToOneField(User, verbose_name="هم تیمی دوم", on_delete=models.CASCADE, related_name="secondTeamMate", default=None, null=True)

class inviteModel(models.Model):
    sender = models.ForeignKey(User, verbose_name="ارسال کننده", on_delete=models.CASCADE, related_name="sender")
    reciver = models.ForeignKey(User, verbose_name="دریافت کننده", on_delete=models.CASCADE, related_name="reciver")
    is_accept = models.BooleanField(default=False, verbose_name="قبول کردن/نکردن")

