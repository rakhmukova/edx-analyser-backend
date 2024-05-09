from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from courses.api.serializers import CourseSerializer
from courses.models import Course


class CourseView(viewsets.GenericViewSet):
    @action(methods=['GET'], detail=False)
    def get_available_courses(self, request):
        user_id = request.user.id
        courses = Course.objects.available_courses(user_id)
        serializer = CourseSerializer(courses, many=True)
        return JsonResponse(data=serializer.data, safe=False)
