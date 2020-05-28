from django.db import models
from django.conf import settings


class Character(models.Model):
    warcraft_logs_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
