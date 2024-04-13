from django.db import models

class PagesPopularityChart(models.Model):
    pass

class PagesPopularity(models.Model):
    # todo: many bytes
    page_link = models.CharField(max_length=500, null=False, blank=False)
    visits_count = models.IntegerField()
    chart = models.ForeignKey(PagesPopularityChart, on_delete=models.CASCADE, related_name='items')
