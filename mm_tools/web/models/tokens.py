from django.db import models
from django.conf import settings


class Token(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    def __str__(self):
        return "{} : {}".format(self.user, self.token)
