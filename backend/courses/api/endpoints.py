from django.urls import path

from courses.api import viewsets

urlpatterns = [
    path('', viewsets.CourseViewSet.as_view({'get': 'get_courses'}))
]
