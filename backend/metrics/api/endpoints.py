from django.urls import path

from metrics.api import viewsets

urlpatterns = [
    path('common/', viewsets.SectionReportViewSet.as_view({'get': 'get_common_section_report'})),
    path('video/', viewsets.SectionReportViewSet.as_view({'get': 'get_video_section_report'})),
    path('textbook/', viewsets.SectionReportViewSet.as_view({'get': 'get_textbook_section_report'})),
    path('problems/', viewsets.SectionReportViewSet.as_view({'get': 'get_task_section_report'})),
    path('pages/', viewsets.SectionReportViewSet.as_view({'get': 'get_pages_section_report'})),
    path('forum/', viewsets.SectionReportViewSet.as_view({'get': 'get_forum_section_report'})),
]
