from rest_framework import serializers

from metrics.models.pages import PagesPopularityChart, PagesPopularity


class PagesPopularitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PagesPopularity
        fields = ['page_link', 'visits_count']


class PagesPopularityChartSerializer(serializers.ModelSerializer):
    items = PagesPopularitySerializer(many=True)

    class Meta:
        model = PagesPopularityChart
        fields = ['items']
