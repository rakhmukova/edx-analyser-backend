from django.http import JsonResponse
from event_logs.api.serializers import UploadedFileSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_serializer = UploadedFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return JsonResponse({'message': 'File uploaded successfully'}, status=201)
        else:
            return JsonResponse(file_serializer.errors, status=400)
