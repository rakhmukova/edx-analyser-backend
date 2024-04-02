from django.db import models

MAX_VIDEO_LINK_LENGTH = 100

class VideoPlayCountChart(models.Model):
    pass

class VideoPlayCount(models.Model):
    date = models.DateField()
    count = models.IntegerField()
    chart = models.ForeignKey(VideoPlayCountChart, on_delete=models.CASCADE, related_name='items')


class VideoInteractionChart(models.Model):
    pass

class VideoInteraction(models.Model):
    video_link = models.CharField(max_length=MAX_VIDEO_LINK_LENGTH)
    students_visits_count = models.IntegerField()
    viewing_percent_median = models.IntegerField()
    chart = models.ForeignKey(VideoInteractionChart, on_delete=models.CASCADE, related_name='items')