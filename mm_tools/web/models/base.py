from django.db import models

MOLTEN_CORE = 'MC'
BLACKWING_LAIR = 'BWL'
ZUL_GURUB = 'ZG'
ONYXIA = 'ONY'
AQ_20 = 'AQ20'
AQ_40 = 'AQ40'
NAXX = 'NAXX'

RAIDS = (
    (MOLTEN_CORE, 'Molten Core'),
    (BLACKWING_LAIR, 'Blackwing Lair'),
    (ZUL_GURUB, 'Zul\'gurub'),
    (ONYXIA, 'Onyxia'),
    (AQ_20, 'Ruins of Ahn\'Qiraj'),
    (AQ_40, 'Temple of Ahn\'Qiraj'),
    (NAXX, 'Naxx')
)

__all__ = [
    'MOLTEN_CORE',
    'BLACKWING_LAIR',
    'ZUL_GURUB',
    'ONYXIA',
    'AQ_20',
    'AQ_40',
    'NAXX',
    'RAIDS',
    'Config'
]


class Config(models.Model):

    key = models.CharField(max_length=50, primary_key=True)
    value = models.CharField(max_length=255)

    @classmethod
    def get(cls, key, default):
        try:
            return Config.objects.get(key=key).value
        except Config.DoesNotExist:
            return default

    @classmethod
    def set(cls, key, value):
        try:
            config = Config.objects.get(key=key)
            config.value = value
            config.save()
        except Config.DoesNotExist:
            config = Config(
                key=key,
                value=value
            ).save()
