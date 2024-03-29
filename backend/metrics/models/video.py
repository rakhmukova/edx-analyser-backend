from django.db import models

from metrics.models.util import MAX_VIDEO_LINK_LENGTH


class DailyPlayVideoCount(models.Model):
    date = models.DateField()
    play_count = models.IntegerField()


class SpecificVideoInteraction(models.Model):
    video_link = models.CharField(max_length=MAX_VIDEO_LINK_LENGTH)
    students_visits_count = models.IntegerField()
    viewing_percent_median = models.IntegerField()
