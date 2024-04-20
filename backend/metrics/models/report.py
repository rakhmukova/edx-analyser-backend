from datetime import datetime
from typing import Any

from django.db import models

from courses.models import Course, MAX_COURSE_ID_LENGTH
from metrics.models.common import SectionActivityChart, WeeklyActivityChart
from metrics.models.forum import ForumQuestionChart
from metrics.models.pages import PagesPopularityChart
from metrics.models.tasks import TaskComplexityChart, TaskSummaryChart
from metrics.models.textbook import WordSearchChart, TextbookViewsChart
from metrics.models.video import VideoInteractionChart, VideoPlayCountChart

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

class ErrorType:
    DB_CONNECTION_ERROR = "db_connection_error"
    INTEGRITY_ERROR = "integrity_error"

    CHOICES = [
        (DB_CONNECTION_ERROR, "db_connection_error"),
        (INTEGRITY_ERROR, "integrity_error"),
    ]


class SectionReport(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, primary_key=True)
    last_time_accessed = models.DateTimeField(default=datetime.now)
    last_time_updated = models.DateTimeField(default=datetime.now)
    report_state = models.CharField(max_length=12, choices=ReportState.CHOICES, null=False, default=ReportState.NOT_STARTED)
    error_code = models.CharField(max_length=50, choices=ReportState.CHOICES, null=True, blank=False, default=None)

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
    students_count = models.PositiveIntegerField(null=True, default=None)
    active_students_count = models.PositiveIntegerField(null=True, default=None)
    section_activity_chart = models.OneToOneField(SectionActivityChart, on_delete=models.CASCADE, null=True, default=None)
    weekly_activity_chart = models.OneToOneField(WeeklyActivityChart, on_delete=models.CASCADE, null=True, default=None)

    def save(self, *args, **kwargs):
        self.report_state = self.calc_report_state(['section_activity_chart', 'weekly_activity_chart', 'students_count', 'active_students_count'])
        super().save(*args, **kwargs)


class TextbookSectionReport(SectionReport):
    textbook_views_chart = models.OneToOneField(TextbookViewsChart, on_delete=models.CASCADE, null=True, default=None)
    word_search_chart = models.OneToOneField(WordSearchChart, on_delete=models.CASCADE, null=True, default=None)
    def save(self, *args, **kwargs):
        self.report_state = self.calc_report_state(['textbook_views_chart', 'word_search_chart'])
        super().save(*args, **kwargs)


class TaskSectionReport(SectionReport):
    task_complexity_chart = models.OneToOneField(TaskComplexityChart, on_delete=models.CASCADE, null=True, default=None)
    task_summary_chart = models.OneToOneField(TaskSummaryChart, on_delete=models.CASCADE, null=True, default=None)
    def save(self, *args, **kwargs):
        self.report_state = self.calc_report_state(['task_complexity_chart', 'task_summary_chart'])
        super().save(*args, **kwargs)

class PagesSectionReport(SectionReport):
    pages_popularity_chart = models.OneToOneField(PagesPopularityChart, on_delete=models.CASCADE, null=True, default=None)
    def save(self, *args, **kwargs):
        self.report_state = self.calc_report_state(['pages_popularity_chart'])
        super().save(*args, **kwargs)


class ForumSectionReport(SectionReport):
    forum_question_chart = models.OneToOneField(ForumQuestionChart, on_delete=models.CASCADE, null=True, default=None)
    def save(self, *args, **kwargs):
        self.report_state = self.calc_report_state(['forum_question_chart'])
        super().save(*args, **kwargs)
