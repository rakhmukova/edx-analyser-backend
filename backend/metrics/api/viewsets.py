from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request

from metrics.api.serializers.report import VideoSectionReportSerializer, \
    CommonSectionReportSerializer, TextbookSectionReportSerializer, TaskSectionReportSerializer, \
    PagesSectionReportSerializer, ForumSectionReportSerializer
from metrics.logic.report_manager import get_report
from metrics.models.section_type import SectionType


class SectionReportViewSet(viewsets.GenericViewSet):
    # todo: check in db
    valid_courses = [
        'DATANTECH2035',
        'DATSTBASE'
    ]

    url_to_serializer ={
        'common': CommonSectionReportSerializer,
        'video': VideoSectionReportSerializer,
        'textbook': TextbookSectionReportSerializer,
        'problems': TaskSectionReportSerializer,
        'pages': PagesSectionReportSerializer,
        'forum': ForumSectionReportSerializer,
    }

    url_to_section_type = {
        'common': SectionType.COMMON,
        'video': SectionType.VIDEO,
        'textbook': SectionType.PDF,
        'problems': SectionType.TASKS,
        'pages': SectionType.PAGES,
        'forum': SectionType.FORUM,
    }

    def _validate_course(self, course_id):
        return course_id in self.valid_courses

    @action(methods=['GET'], detail=False)
    def get_section_report(self, request: Request, course_id=None, section_type=None):
        force_update = request.query_params.get('force-update', False)
        if not self._validate_course(course_id):
            return JsonResponse({'error': f'Invalid course_id: {course_id}'}, status=status.HTTP_400_BAD_REQUEST)

        if not self.url_to_serializer[section_type] or not self.url_to_section_type[section_type]:
            return JsonResponse({'error': 'Invalid section type'}, status=status.HTTP_400_BAD_REQUEST)

        report = get_report(course_id, self.url_to_section_type[section_type], force_update)
        serializer = self.url_to_serializer[section_type](report, many=False)
        return JsonResponse(data=serializer.data)
