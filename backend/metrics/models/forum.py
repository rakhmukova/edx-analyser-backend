from django.db import models


class QuestionType:
    THREAD = "thread"
    RESPONSE = "response"
    CHOICES = [
        (THREAD, "Thread"),
        (RESPONSE, "Response")
    ]


# class ForumQuestionChart(models.Model):
#     pass
#
#
# class ForumQuestion(models.Model):
#     title = models.TextField()
#     likes_count = models.IntegerField(default=0)
#     comments_count = models.IntegerField(default=0)
#     question_type = models.CharField(choices=QuestionType.CHOICES)
#     chart = models.ForeignKey(ForumQuestionChart, on_delete=models.CASCADE, related_name="items")
