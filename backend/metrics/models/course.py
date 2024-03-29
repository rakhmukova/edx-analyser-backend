from django.db import models


class SessionAverageTime(models.Model):
    session_type = models.CharField(max_length=20)
    average_time = models.IntegerField()