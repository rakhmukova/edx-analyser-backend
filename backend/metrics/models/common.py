from django.core.validators import MinValueValidator, MaxValueValidator
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


class CompletionDegreeChart(models.Model):
    pass

class CompletionDegree(models.Model):
    completion_degree = models.CharField(max_length=12, choices=CompletionType.CHOICES, default=CompletionType.NOT_STARTED)
    students_count = models.IntegerField()
    chart = models.ForeignKey(CompletionDegreeChart, on_delete=models.CASCADE, related_name='items')


class SessionTimeChart(models.Model):
    pass

class SessionTime(models.Model):
    session_type = models.CharField(max_length=10, choices=SessionType.CHOICES, default=SessionType.ALL)
    average_time = models.IntegerField()
    chart = models.ForeignKey(SessionTimeChart, on_delete=models.CASCADE, related_name='items')


class SectionActivityChart(models.Model):
    pass

class SectionActivity(models.Model):
    section_type = models.CharField(max_length=10, choices=SectionType.CHOICES)
    students_percent = models.IntegerField()
    chart = models.ForeignKey(SectionActivityChart, on_delete=models.CASCADE, related_name='items')


# class WeeklyActivity(models.Model):
