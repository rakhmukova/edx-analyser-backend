from rest_framework.generics import RetrieveAPIView, ListAPIView

from courses.api.serializers import CourseSerializer
from courses.models import Course


class CourseView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
