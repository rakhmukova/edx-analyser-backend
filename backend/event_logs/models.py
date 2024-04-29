import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible

from app import settings


class LogProcessingStatus:
    PROCESSING = "Processing"
    COMPLETED = "Completed"

    CHOICES = (
        (PROCESSING, "Processing"),
        (COMPLETED, "Completed")
    )


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid.uuid4(), ext)
        return os.path.join(self.path, filename)


path_and_rename = PathAndRename(settings.ZIP_LOG_ARCHIVES_FOLDER)


class LogsArchive(models.Model):
    archive = models.FileField(upload_to=path_and_rename)
    processing_status = models.CharField(choices=LogProcessingStatus.CHOICES, max_length=15, null=False, blank=False)
    original_log_name = models.CharField(max_length=100, null=False, blank=False)

    @property
    def archive_name(self) -> str:
        # /a/b/c/a9e05699-d3cf-40d6-a01c-3a74efbc5fad.zip -> a9e05699-d3cf-40d6-a01c-3a74efbc5fad
        return os.path.basename(self.archive.name).split('.')[0]

    @property
    def zst_folder_path(self) -> str:
        return os.path.join(settings.ZST_LOGS_FOLDER, self.archive_name)

    @property
    def logs_folder_path(self) -> str:
        return os.path.join(settings.PURE_LOGS_FOLDER, self.archive_name)
