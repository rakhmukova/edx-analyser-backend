from rest_framework import serializers

from event_logs.models import LogsArchive, LogProcessingStatus
from event_logs.tasks import unzip_logs_archive_task


class LogsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogsArchive
        fields = ['archive', 'original_log_name', 'processing_status']
        read_only_fields = ['original_log_name', 'processing_status']
        extra_kwargs = {'archive': {'write_only': True}}

    def save(self, **kwargs):
        logs_archive = super(LogsFileSerializer, self).save(**kwargs,
                                             original_log_name=self.validated_data['archive'].name,
                                             processing_status=LogProcessingStatus.PROCESSING)
        print("saved")
        unzip_logs_archive_task.apply_async(kwargs={'log_id': logs_archive.id})
        return logs_archive
