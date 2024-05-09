from django.urls import path
from event_logs.api.views import LogsUploadView

urlpatterns = [
    path('', LogsUploadView.as_view(), name='file-upload'),
]
