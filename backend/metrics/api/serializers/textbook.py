from rest_framework import serializers

from metrics.models.textbook import WordSearchChart, TextbookViewsChart, WordSearchCount, TextbookViewsCount


class WordSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordSearchCount
        fields = ['word', 'search_count']


class TextbookViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextbookViewsCount
        fields = ['pdf_name', 'views_count', 'unique_students_count']


class WordSearchChartSerializer(serializers.ModelSerializer):
    items = WordSearchSerializer(many=True)

    class Meta:
        model = WordSearchChart
        fields = ['items']


class TextbookViewsChartSerializer(serializers.ModelSerializer):
    items = TextbookViewsSerializer(many=True)

    class Meta:
        model = TextbookViewsChart
        fields = ['items']
