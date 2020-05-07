from django.db import models
from django.conf import settings


RAIDS = (
    ('MC', 'Molten Core'),
    ('BWL', 'Blackwing Lair'),
    ('ZG', 'Zul\'gurub')
)


class Item(models.Model):
    zone = models.CharField(choices=RAIDS, max_length=5)
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    slot = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Priority(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        permissions = [('can_export_priorities', 'Can export priorities')]