from django.urls import path
from event_logs.views import FileUploadView

urlpatterns = [
    path('', FileUploadView.as_view(), name='file-upload'),
]
