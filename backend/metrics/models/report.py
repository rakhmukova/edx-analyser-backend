from datetime import datetime

from django.db import models

from metrics.models.report_state import ReportState
from metrics.models.util import MAX_COURSE_ID_LENGTH


# нужны ли разные модели если все они хранят json поле с информацией
class CourseReport(models.Model):
    course_id = models.CharField(max_length=MAX_COURSE_ID_LENGTH)
    last_time_accessed = models.DateTimeField(default=datetime.now)
    last_time_updated = models.DateTimeField(default=datetime.now)
    report_state = models.CharField(max_length=12, choices=ReportState.CHOICES, default=ReportState.DEFAULT)

    class Meta:
        abstract = True


class VideoSectionReport(CourseReport):
    video_report_data = models.JSONField(default=dict)


class CommonSectionReport(CourseReport):
    common_report_data = models.JSONField(default=dict)
