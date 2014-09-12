from django.db import models
# from django.contrib import admin

class account_data(models.Model):
    username = models.CharField(max_length=30)
    key = models.CharField(max_length=30)
    value = models.CharField(max_length=500, null=True, blank=True)
    class Meta:
        unique_together = ("username", "key")