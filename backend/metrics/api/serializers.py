from rest_framework import serializers

from metrics.models.report import VideoSectionReport, CommonSectionReport


class CommonSectionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonSectionReport
        fields = ['course_id', 'last_time_accessed','last_time_updated', 'report_state', 'common_report_data']



class VideoSectionReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoSectionReport
        fields = ['course_id', 'last_time_accessed','last_time_updated', 'report_state', 'video_report_data']
