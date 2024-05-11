from django.db import models

from metrics.models.section_type import SectionType


class SessionType:
    BROWSER = "browser"
    MOBILE = "mobile"
    ALL = "all"
    CHOICES = [
        (BROWSER, "Browser"),
        (MOBILE, "Mobile"),
        (ALL, "All types"),
    ]


class CompletionType:
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

    CHOICES = [
        (NOT_STARTED, "Not started"),
        (IN_PROGRESS, "In progress"),
        (COMPLETED, "Completed"),
    ]


class SectionActivityChart(models.Model):
    pass


class SectionActivity(models.Model):
    section_type = models.CharField(max_length=10, choices=SectionType.CHOICES)
    students_count = models.PositiveIntegerField(default=0)
    chart = models.ForeignKey(SectionActivityChart, on_delete=models.CASCADE, related_name='items')


class WeeklyActivityChart(models.Model):
    pass


class WeeklyActivityCount(models.Model):
    date = models.DateField()
    count = models.PositiveIntegerField()
    chart = models.ForeignKey(WeeklyActivityChart, on_delete=models.CASCADE, related_name='items')
