from rest_framework import serializers

from metrics.models.report import SectionReport


class SectionReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = SectionReport
        fields = ['course_id', 'section_type', 'last_time_accessed','last_time_updated', 'report_state', 'report_data']
