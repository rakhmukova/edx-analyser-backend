from django.contrib import admin

from metrics.models.report import VideoSectionReport, CommonSectionReport


# Register your models here.
@admin.register(VideoSectionReport)
class VideoSectionReportAdmin(admin.ModelAdmin):
    list_display = ["course_id", "last_time_accessed", "last_time_updated"]

@admin.register(CommonSectionReport)
class CommonSectionReportAdmin(admin.ModelAdmin):
    list_display = ["course_id", "last_time_accessed", "last_time_updated"]

