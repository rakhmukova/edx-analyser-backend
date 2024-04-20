from django.contrib import admin

from metrics.models.report import VideoSectionReport, CommonSectionReport, TextbookSectionReport, TaskSectionReport, \
    PagesSectionReport, ForumSectionReport


@admin.register(CommonSectionReport)
class CommonSectionReportAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'last_time_accessed', 'last_time_updated', 'report_state']


@admin.register(VideoSectionReport)
class VideoSectionReportAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'last_time_accessed', 'last_time_updated', 'report_state']

@admin.register(TextbookSectionReport)
class TextbookSectionReportAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'last_time_accessed', 'last_time_updated', 'report_state', 'textbook_views_chart', 'word_search_chart']

@admin.register(TaskSectionReport)
class TaskSectionReportAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'last_time_accessed', 'last_time_updated', 'report_state', 'task_complexity_chart', 'task_summary_chart']

@admin.register(PagesSectionReport)
class PagesSectionReportAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'last_time_accessed', 'last_time_updated', 'report_state']

@admin.register(ForumSectionReport)
class ForumSectionReportAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'last_time_accessed', 'last_time_updated', 'report_state']
