from django.db import models
from django.conf import settings
from .characters import Character
from .items import Item


__all__ = [
    'Raid',
    'Boss',
    'BossFight',
    'LootAwarded'
]


class Raid(models.Model):
    warcraft_logs_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    started_on = models.DateTimeField()
    ended_on = models.DateTimeField()
    zone = models.IntegerField()

    def __str__(self):
        return "{} : {} @ {}".format(self.warcraft_logs_id, self.title, self.started_on.strftime("%b %d %Y %H:%M:%S"))

    class Meta:
        ordering = ['-started_on']


class Boss(models.Model):
    warcraft_logs_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BossFight(models.Model):
    raid = models.ForeignKey(Raid, on_delete=models.CASCADE)
    fight_index = models.IntegerField()
    boss = models.ForeignKey(Boss, on_delete=models.CASCADE)
    kill = models.BooleanField()
    started_on = models.DateTimeField()
    ended_on = models.DateTimeField()
    attendance = models.ManyToManyField(Character)

    def __str__(self):
        return self.boss.name


class LootAwarded(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    raid = models.ForeignKey(Raid, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Loot awarded"
        unique_together = ['item', 'character', 'raid']
        ordering = ['-raid__started_on', 'character__name']
