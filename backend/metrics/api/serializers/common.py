from rest_framework import serializers

from metrics.models.common import CompletionDegree, SessionTime, SectionActivity, CompletionDegreeChart, \
    SessionTimeChart, SectionActivityChart


class CompletionDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletionDegree
        fields = ['completion_degree', 'students_count']

class SessionTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionTime
        fields = ['session_type', 'average_time']

class SectionActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionActivity
        fields = ['section_type', 'students_percent']

class CompletionDegreeChartSerializer(serializers.ModelSerializer):
    items = CompletionDegreeSerializer(many=True)
    class Meta:
        model = CompletionDegreeChart
        fields = ['items']

class SessionTimeChartSerializer(serializers.ModelSerializer):
    items = SessionTimeSerializer(many=True)
    class Meta:
        model = SessionTimeChart
        fields = ['items']

class SectionActivityChartSerializer(serializers.ModelSerializer):
    items = SectionActivitySerializer(many=True)
    class Meta:
        model = SectionActivityChart
        fields = ['items']
