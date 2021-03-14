from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone


class RouterList(models.Model):
    name = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=24)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    routerboard = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name