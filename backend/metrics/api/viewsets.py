from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request

from courses.models import Course
from metrics.api.serializers.report import VideoSectionReportSerializer, \
    CommonSectionReportSerializer, TextbookSectionReportSerializer, TaskSectionReportSerializer, \
    PagesSectionReportSerializer, ForumSectionReportSerializer
from metrics.logic.report_manager import get_report
from metrics.models.section_type import SectionType


class SectionReportViewSet(viewsets.GenericViewSet):
    # todo: remove
    short_names_to_ids = {
        'DATANTECH2035': 'course-v1:ITMOUniversity+DATANTECH2035+summer_2022_1',
        'DATSTBASE': 'course-v1:ITMOUniversity+DATSTBASE+spring_2024_ITMO_bac',
        'DATSTPRO': 'course-v1:ITMOUniversity+DATSTPRO+spring_2024_ITMO_bac'
    }

    url_to_serializer = {
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

    def _validate_course(self, course_id: str, user_id: int):
        return Course.objects.available_courses(user_id).filter(course_id=course_id).exists()

    @action(methods=['GET'], detail=False)
    def get_section_report(self, request: Request, course_id=None, section_type=None) -> JsonResponse:
        if course_id in self.short_names_to_ids:
            course_id = self.short_names_to_ids[course_id]

        user_id = request.user.id

        if not self._validate_course(course_id, user_id):
            return JsonResponse({'error': f'No course with such course id: {course_id}'},
                                status=status.HTTP_404_NOT_FOUND)

        if not self.url_to_serializer[section_type] or not self.url_to_section_type[section_type]:
            return JsonResponse({'error': 'Invalid section type'}, status=status.HTTP_400_BAD_REQUEST)

        force_update = request.query_params.get('force-update', False)
        report = get_report(course_id, user_id, self.url_to_section_type[section_type], force_update)
        serializer = self.url_to_serializer[section_type](report, many=False)
        return JsonResponse(data=serializer.data)
