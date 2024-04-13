from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from metrics.api.serializers.report import VideoSectionReportSerializer, \
    CommonSectionReportSerializer, TextbookSectionReportSerializer, TaskSectionReportSerializer, \
    PagesSectionReportSerializer, ForumSectionReportSerializer
from metrics.logic.report_manager import get_report
from metrics.models.section_type import SectionType


class SectionReportViewSet(viewsets.GenericViewSet):
    @action(methods=['GET'], detail=False)
    def get_common_section_report(self, request, course_id=None) -> Response:
        report = get_report(course_id, SectionType.COMMON)
        serializer = CommonSectionReportSerializer(report, many=False)
        return Response(data=serializer.data)

    @action(methods=['GET'], detail=False)
    def get_video_section_report(self, request, course_id=None) -> Response:
        report = get_report(course_id, SectionType.VIDEO)
        serializer = VideoSectionReportSerializer(report, many=False)
        return Response(data=serializer.data)

    @action(methods=['GET'], detail=False)
    def get_textbook_section_report(self, request, course_id=None) -> Response:
        report = get_report(course_id, SectionType.PDF)
        serializer = TextbookSectionReportSerializer(report, many=False)
        return Response(data=serializer.data)

    @action(methods=['GET'], detail=False)
    def get_task_section_report(self, request, course_id=None) -> Response:
        report = get_report(course_id, SectionType.TASKS)
        serializer = TaskSectionReportSerializer(report, many=False)
        return Response(data=serializer.data)

    @action(methods=['GET'], detail=False)
    def get_pages_section_report(self, request, course_id=None) -> Response:
        report = get_report(course_id, SectionType.PAGES)
        serializer = PagesSectionReportSerializer(report, many=False)
        return Response(data=serializer.data)

    @action(methods=['GET'], detail=False)
    def get_forum_section_report(self, request, course_id=None) -> Response:
        report = get_report(course_id, SectionType.FORUM)
        serializer = ForumSectionReportSerializer(report, many=False)
        return Response(data=serializer.data)
