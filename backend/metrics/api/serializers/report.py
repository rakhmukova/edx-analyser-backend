from rest_framework import serializers

from metrics.api.serializers.common import CompletionDegreeChartSerializer, SessionTimeChartSerializer, \
    SectionActivityChartSerializer
from metrics.api.serializers.video import VideoPlayCountChartSerializer, VideoInteractionChartSerializer
from metrics.models.report import SectionReport, VideoSectionReport, CommonSectionReport


class SectionReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = SectionReport
        abstract = True
        fields = ['course_id', 'last_time_accessed', 'last_time_updated', 'report_state']

class VideoSectionReportSerializer(SectionReportSerializer):
    video_play_count_chart = VideoPlayCountChartSerializer()
    video_interaction_chart = VideoInteractionChartSerializer()

    class Meta:
        model = VideoSectionReport
        fields = SectionReportSerializer.Meta.fields + ['video_play_count_chart', 'video_interaction_chart']

class CommonSectionReportSerializer(SectionReportSerializer):
    completion_degree_chart = CompletionDegreeChartSerializer()
    session_time_chart = SessionTimeChartSerializer()
    section_activity_chart = SectionActivityChartSerializer()

    class Meta:
        model = CommonSectionReport
        fields = SectionReportSerializer.Meta.fields + ['completion_degree_chart', 'session_time_chart', 'section_activity_chart']
