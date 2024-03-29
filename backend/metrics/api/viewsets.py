from datetime import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from metrics.api.serializers import VideoSectionReportSerializer
from metrics.models.report import VideoSectionReport, CommonSectionReport


class SectionReportViewSet(viewsets.GenericViewSet):
    @action(methods=['GET'], detail=False)
    def get_common_section_report(self, request, course_id=None) -> Response:
        result = CommonSectionReport(
            course_id=course_id,
            last_time_accessed=datetime.now(),
            last_time_updated=datetime.now(),
        )
        serializer = VideoSectionReportSerializer(result, many=False)
        return Response(data=serializer.data)

    @action(methods=['GET'], detail=False)
    def get_video_section_report(self, request, course_id=None) -> Response:
        result = VideoSectionReport(
            course_id=course_id,
            last_time_accessed=datetime.now(),
            last_time_updated=datetime.now(),
        )
        serializer = VideoSectionReportSerializer(result, many=False)
        return Response(data=serializer.data)
