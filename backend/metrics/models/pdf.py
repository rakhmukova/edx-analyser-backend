from django.db import models


# class DocumentViewsChart(models.Model):
#     pass
#
# class DocumentViewsCount(models.Model):
#     pdf_name = models.CharField(max_length=200)
#     views_count = models.IntegerField()
#     time_spent_median = models.IntegerField()
#     chart = models.ForeignKey(DocumentViewsChart, on_delete=models.CASCADE)
#
#
# class WordSearchChart(models.Model):
#     pass
#
# class WordSearchCount(models.Model):
#     word = models.CharField(max_length=100, blank=False, null=False)
#     search_count = models.IntegerField()
#     chart = models.ForeignKey(WordSearchChart, on_delete=models.CASCADE)
