from django.urls import path

from metrics.api import viewsets

urlpatterns = [
    path('<str:section_type>/',
         viewsets.SectionReportViewSet.as_view({'get': 'get_section_report'})),
]
