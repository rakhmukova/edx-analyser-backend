from rest_framework import serializers

from metrics.models.students import StudentData, StudentsChart


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = ['username', 'total_days', 'total_hours', 'video_views',
                  'textbook_views', 'solved_tasks', 'average_attempt_count', 'forum_activity']


class StudentChartSerializer(serializers.ModelSerializer):
    items = StudentSerializer(many=True)

    class Meta:
        model = StudentsChart
        fields = ['items']
