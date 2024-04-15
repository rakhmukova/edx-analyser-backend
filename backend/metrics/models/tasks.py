from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class AttemptCount:
    FIRST_ATTEMPT = "first"
    SECOND_ATTEMPT = "second"
    MORE_ATTEMPTS = "more"
    CHOICES = [
        (FIRST_ATTEMPT, "First attempt"),
        (SECOND_ATTEMPT, "Second attempt"),
        (MORE_ATTEMPTS, "Third attempt and more")
    ]


class TaskComplexityChart(models.Model):
    pass

class TaskComplexity(models.Model):
    problem_link = models.CharField(max_length=250)
    all_attempts = models.IntegerField()
    successful_attempts = models.IntegerField()
    chart = models.ForeignKey(TaskComplexityChart, on_delete=models.CASCADE, related_name='items')

class TaskSummaryChart(models.Model):
    pass

class TaskSummary(models.Model):
    attempt_count = models.CharField(choices=AttemptCount.CHOICES)
    percentage = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    chart = models.ForeignKey(TaskSummaryChart, on_delete=models.CASCADE, related_name='items')
