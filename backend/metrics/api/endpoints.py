from django.urls import path

from metrics.api import viewsets

urlpatterns = [
    path('common/', viewsets.SectionReportViewSet.as_view({'get': 'get_common_section_report'})),
    path('video/', viewsets.SectionReportViewSet.as_view({'get': 'get_video_section_report'})),
]
