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

#
# class TaskComplexityChart(models.Model):
#     pass
#
# class TaskComplexity(models.Model):
#     task_id = models.CharField(max_length=250)
#     successful_solutions_median = models.IntegerField(
#         validators=[
#             MinValueValidator(0),
#             MaxValueValidator(100)
#         ]
#     )
#     chart = models.ForeignKey(TaskComplexityChart, on_delete=models.CASCADE, related_name='items')
#
# class TasksAttemptCountChart(models.Model):
#     pass
#
# class TasksAttemptCount(models.Model):
#     attempt_count = models.CharField()
#     percentage = models.IntegerField(
#         validators=[
#             MinValueValidator(0),
#             MaxValueValidator(100)
#         ]
#     )
#     chart = models.ForeignKey(TasksAttemptCountChart, on_delete=models.CASCADE, related_name='items')

