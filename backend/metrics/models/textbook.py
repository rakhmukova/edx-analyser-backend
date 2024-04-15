from django.db import models


class TextbookViewsChart(models.Model):
    pass

class TextbookViewsCount(models.Model):
    pdf_name = models.CharField(max_length=200)
    views_count = models.PositiveIntegerField()
    unique_students_count = models.PositiveIntegerField()
    chart = models.ForeignKey(TextbookViewsChart, on_delete=models.CASCADE, related_name='items')


class WordSearchChart(models.Model):
    pass

class WordSearchCount(models.Model):
    word = models.CharField(max_length=100, blank=False, null=False)
    search_count = models.PositiveIntegerField()
    chart = models.ForeignKey(WordSearchChart, on_delete=models.CASCADE, related_name='items')
