from datetime import datetime

from django.db import models

from metrics.models.report_state import ReportState
from metrics.models.section_type import SectionType
from metrics.models.util import MAX_COURSE_ID_LENGTH


class SectionReport(models.Model):
    course_id = models.CharField(max_length=MAX_COURSE_ID_LENGTH, null=False, blank=False)
    section_type = models.CharField(max_length=10, choices=SectionType.CHOICES, null=False, blank=False)
    last_time_accessed = models.DateTimeField(default=datetime.now)
    last_time_updated = models.DateTimeField(default=datetime.now)
    report_state = models.CharField(max_length=12, choices=ReportState.CHOICES)
    report_data = models.JSONField(default=dict)

    class Meta:
        unique_together = ('course_id', 'section_type')
