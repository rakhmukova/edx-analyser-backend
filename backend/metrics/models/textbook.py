from django.db import models


class TextbookViewsChart(models.Model):
    pass

class TextbookViewsCount(models.Model):
    pdf_name = models.CharField(max_length=200)
    views_count = models.IntegerField()
    unique_students_count = models.IntegerField()
    chart = models.ForeignKey(TextbookViewsChart, on_delete=models.CASCADE)


class WordSearchChart(models.Model):
    pass

class WordSearchCount(models.Model):
    word = models.CharField(max_length=100, blank=False, null=False)
    search_count = models.IntegerField()
    chart = models.ForeignKey(WordSearchChart, on_delete=models.CASCADE)
