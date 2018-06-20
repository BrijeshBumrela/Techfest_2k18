from django.db import models

from django.contrib.auth.models import User


# Create your models here.

class MoreUserData(models.Model):
    user = models.OneToOneField(to=User, primary_key=True, on_delete=models.CASCADE)
    college_name = models.CharField(verbose_name="College Name", max_length=100)
    github_id = models.CharField(verbose_name="Github Username", max_length=50, blank=True)
    hackerrank_id = models.CharField(verbose_name="Hackerrank Username", max_length=50, blank=True)
    codechef_id = models.CharField(verbose_name="Codechef Username", max_length=50, blank=True)
    codeforces_id = models.CharField(verbose_name="Codeforces Username", max_length=50, blank=True)
