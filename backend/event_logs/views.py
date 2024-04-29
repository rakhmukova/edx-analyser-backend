from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser

from event_logs.api.serializers import LogsFileSerializer
from event_logs.models import LogsArchive


class LogsUploadView(CreateAPIView):
    queryset = LogsArchive.objects.all()
    serializer_class = LogsFileSerializer
    parser_classes = [MultiPartParser]
