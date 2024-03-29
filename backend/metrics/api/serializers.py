from rest_framework import serializers

from metrics.models.report import VideoSectionReport


class VideoSectionReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoSectionReport
        fields = ['course_id', 'last_time_accessed','last_time_updated']
