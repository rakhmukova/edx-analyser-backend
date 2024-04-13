from rest_framework import serializers

from metrics.models.tasks import TaskComplexityChart, TaskSummaryChart, TaskComplexity, TaskSummary


class TaskComplexitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComplexity
        fields = ['problem_link', 'all_attempts', 'successful_attempts']

class TaskSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSummary
        fields = ['attempt_count', 'percentage']


class TaskComplexityChartSerializer(serializers.ModelSerializer):
    items = TaskComplexitySerializer(many=True)

    class Meta:
        model = TaskComplexityChart
        fields = ['items']

class TaskSummaryChartSerializer(serializers.ModelSerializer):
    items = TaskSummarySerializer(many=True)

    class Meta:
        model = TaskSummaryChart
        fields = ['items']
