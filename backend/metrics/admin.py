from django.contrib import admin

from metrics.models.report import SectionReport


# Register your models here.
@admin.register(SectionReport)
class SectionReportAdmin(admin.ModelAdmin):
    list_display = ["course_id", "last_time_accessed", "last_time_updated", "report_state", "report_data"]
