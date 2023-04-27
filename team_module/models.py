from django.db import models
from account_module.models import User

# Create your models here.
class teamsModel(models.Model):
    teamName = models.CharField(verbose_name="نام تیم", max_length=200)
    capitan = models.ForeignKey(User, verbose_name="کاپیتان", on_delete=models.CASCADE, related_name="captian")
    teamMate1 = models.ForeignKey(User, verbose_name="هم تیمی اول", on_delete=models.CASCADE, related_name="firstTeamMate", default=None, null=True, unique=True)
    teamMate2 = models.ForeignKey(User, verbose_name="هم تیمی دوم", on_delete=models.CASCADE, related_name="secondTeamMate", default=None, null=True, unique=True)

