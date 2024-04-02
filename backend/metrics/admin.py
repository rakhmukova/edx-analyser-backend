from django.contrib import admin

from metrics.models.report import VideoSectionReport, CommonSectionReport


@admin.register(VideoSectionReport)
class VideoSectionReportAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'last_time_accessed', 'last_time_updated', 'report_state']

@admin.register(CommonSectionReport)
class CommonSectionReportAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'last_time_accessed', 'last_time_updated', 'report_state']
