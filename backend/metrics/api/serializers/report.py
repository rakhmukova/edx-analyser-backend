from rest_framework import serializers

from metrics.api.serializers.common import SectionActivityChartSerializer, WeeklyActivityChartSerializer
from metrics.api.serializers.forum import ForumQuestionChartSerializer
from metrics.api.serializers.pages import PagesPopularityChartSerializer
from metrics.api.serializers.tasks import TaskComplexityChartSerializer, TaskSummaryChartSerializer
from metrics.api.serializers.textbook import WordSearchChartSerializer, TextbookViewsChartSerializer
from metrics.api.serializers.video import VideoPlayCountChartSerializer, VideoInteractionChartSerializer
from metrics.models.report import SectionReport, VideoSectionReport, CommonSectionReport, ForumSectionReport, \
    PagesSectionReport, TaskSectionReport, TextbookSectionReport


class SectionReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = SectionReport
        abstract = True
        fields = ['course_id', 'last_time_accessed', 'last_time_updated', 'report_state']

class VideoSectionReportSerializer(SectionReportSerializer):
    video_play_count_chart = VideoPlayCountChartSerializer()
    video_interaction_chart = VideoInteractionChartSerializer()

    class Meta:
        model = VideoSectionReport
        fields = SectionReportSerializer.Meta.fields + ['video_play_count_chart', 'video_interaction_chart']

class CommonSectionReportSerializer(SectionReportSerializer):
    weekly_activity_chart = WeeklyActivityChartSerializer()
    section_activity_chart = SectionActivityChartSerializer()

    class Meta:
        model = CommonSectionReport
        fields = SectionReportSerializer.Meta.fields + ['weekly_activity_chart', 'section_activity_chart', 'students_count']

class TextbookSectionReportSerializer(SectionReportSerializer):
    textbook_views_chart = TextbookViewsChartSerializer()
    word_search_chart = WordSearchChartSerializer()

    class Meta:
        model = TextbookSectionReport
        fields = SectionReportSerializer.Meta.fields + ['textbook_views_chart', 'word_search_chart']


class TaskSectionReportSerializer(SectionReportSerializer):
    task_complexity_chart = TaskComplexityChartSerializer()
    task_summary_chart = TaskSummaryChartSerializer()

    class Meta:
        model = TaskSectionReport
        fields = SectionReportSerializer.Meta.fields + ['task_complexity_chart', 'task_summary_chart']


class PagesSectionReportSerializer(SectionReportSerializer):
    pages_popularity_chart = PagesPopularityChartSerializer()

    class Meta:
        model = PagesSectionReport
        fields = SectionReportSerializer.Meta.fields + ['pages_popularity_chart']


class ForumSectionReportSerializer(SectionReportSerializer):
    forum_question_chart = ForumQuestionChartSerializer()

    class Meta:
        model = ForumSectionReport
        fields = SectionReportSerializer.Meta.fields + ['forum_question_chart']
