from django.db import models
# from django.contrib import admin

class account_data(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    key = models.CharField(max_length=30, primary_key=True)
    value = models.CharField(max_length=30, null=True, blank=True)
