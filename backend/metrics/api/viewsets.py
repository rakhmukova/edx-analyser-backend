from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from metrics.api.serializers import VideoSectionReportSerializer, CommonSectionReportSerializer
from metrics.manager.report_manager import ReportManager
from metrics.models.section_type import SectionType

report_manager = ReportManager()


# todo: choose serialized based on section type as well
class SectionReportViewSet(viewsets.GenericViewSet):
    @action(methods=['GET'], detail=False)
    def get_common_section_report(self, request, course_id=None) -> Response:
        report = report_manager.get_report(course_id, SectionType.COMMON)
        serializer = CommonSectionReportSerializer(report, many=False)
        return Response(data=serializer.data)

    @action(methods=['GET'], detail=False)
    def get_video_section_report(self, request, course_id=None) -> Response:
        report = report_manager.get_report(course_id, SectionType.VIDEO)
        serializer = VideoSectionReportSerializer(report, many=False)
        return Response(data=serializer.data)
