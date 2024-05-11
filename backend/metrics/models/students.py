from django.db import models


class StudentsChart(models.Model):
    pass


class StudentData(models.Model):
    username = models.CharField()
    total_days = models.PositiveIntegerField(default=0)
    total_hours = models.PositiveIntegerField(default=0)
    video_views = models.PositiveIntegerField(default=0)
    textbook_views = models.PositiveIntegerField(default=0)
    solved_tasks = models.PositiveIntegerField(default=0)
    average_attempt_count = models.PositiveIntegerField(default=0)
    forum_activity = models.PositiveIntegerField(default=0)
    chart = models.ForeignKey(StudentsChart, on_delete=models.CASCADE, related_name='items')
