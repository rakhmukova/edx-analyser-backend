from django.db import models


class QuestionType:
    THREAD = "thread"
    RESPONSE = "response"
    CHOICES = [
        (THREAD, "Thread"),
        (RESPONSE, "Response")
    ]


class ForumQuestionChart(models.Model):
    pass


class ForumQuestion(models.Model):
    author = models.CharField()
    title = models.TextField(blank=True, default='')
    body = models.TextField(blank=True, default='')
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    question_type = models.CharField(choices=QuestionType.CHOICES)
    chart = models.ForeignKey(ForumQuestionChart, on_delete=models.CASCADE, related_name="items")
