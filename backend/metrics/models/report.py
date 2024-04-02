from datetime import datetime
from typing import Any

from django.db import models

from metrics.models.common import CompletionDegreeChart, SessionTimeChart, SectionActivityChart
from metrics.models.video import VideoInteractionChart, VideoPlayCountChart

MAX_COURSE_ID_LENGTH = 150


MetricDataType = list[dict[str, Any]]


# store fail reason?
class ReportState:
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    CREATED = "done"
    FAILED = "failed"
    CHOICES = [
        (NOT_STARTED, "Not started"),
        (IN_PROGRESS, "In progress"),
        (CREATED, "Created"),
        (FAILED, "Failed")
    ]


class SectionReport(models.Model):
    course_id = models.CharField(primary_key=True, max_length=MAX_COURSE_ID_LENGTH, null=False, blank=False)
    last_time_accessed = models.DateTimeField(default=datetime.now)
    last_time_updated = models.DateTimeField(default=datetime.now)
    report_state = models.CharField(max_length=12, choices=ReportState.CHOICES, null=False, default=ReportState.NOT_STARTED)
    error_reason = models.CharField(max_length=100, null=True, blank=False, default=None)

    def any_field_is_none(self, fields: list[str]):
        for field_name in fields:
            field_value = getattr(self, field_name)
            if field_value is None:
                return True
        return False

    def calc_report_state(self, fields: list[str]):
        if self.any_field_is_none(fields):
            return ReportState.IN_PROGRESS
        else:
            return ReportState.CREATED

    class Meta:
        abstract = True


class VideoSectionReport(SectionReport):
    video_play_count_chart = models.OneToOneField(VideoPlayCountChart, on_delete=models.CASCADE, null=True, default=None)
    video_interaction_chart = models.OneToOneField(VideoInteractionChart, on_delete=models.CASCADE, null=True, default=None)

    def save(self, *args, **kwargs):
        self.report_state = self.calc_report_state(['video_play_count_chart', 'video_interaction_chart'])
        super().save(*args, **kwargs)


class CommonSectionReport(SectionReport):
    completion_degree_chart = models.OneToOneField(CompletionDegreeChart, on_delete=models.CASCADE, null=True, default=None)
    session_time_chart = models.OneToOneField(SessionTimeChart, on_delete=models.CASCADE, null=True, default=None)
    section_activity_chart = models.OneToOneField(SectionActivityChart, on_delete=models.CASCADE, null=True, default=None)

    def save(self, *args, **kwargs):
        self.report_state = self.calc_report_state(['completion_degree_chart', 'session_time_chart', 'section_activity_chart'])
        super().save(*args, **kwargs)


# class DocumentSectionReport(SectionReport):
#     pdf_views_chart = models.OneToOneField(DocumentViewsChart, on_delete=models.CASCADE)
#     word_search_chart = models.OneToOneField(WordSearchChart, on_delete=models.CASCADE)


# class TaskSectionReport(SectionReport):
#     pass
#
#
# class ForumSectionReport(SectionReport):
#     pass
#
# class PageSectionReport(SectionReport):
#     pass
