from rest_framework import serializers

from metrics.models.common import SectionActivity, \
    SectionActivityChart, WeeklyActivityChart, WeeklyActivityCount


class SectionActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionActivity
        fields = ['section_type', 'students_count']


class WeeklyActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyActivityCount
        fields = ['date', 'count']

class SectionActivityChartSerializer(serializers.ModelSerializer):
    items = SectionActivitySerializer(many=True)
    class Meta:
        model = SectionActivityChart
        fields = ['items']

class WeeklyActivityChartSerializer(serializers.ModelSerializer):
    items = WeeklyActivitySerializer(many=True)

    class Meta:
        model = WeeklyActivityChart
        fields = ['items']
