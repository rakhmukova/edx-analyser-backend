from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request

from courses.api.serializers import CourseSerializer
from courses.models import Course


class CourseViewSet(viewsets.GenericViewSet):
    @action(methods=['GET'], detail=False)
    def get_courses(self, request: Request) -> JsonResponse:
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return JsonResponse(data=serializer.data, safe=False)
