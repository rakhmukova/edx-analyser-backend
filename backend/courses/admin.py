
from django.contrib import admin

from courses.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'name', 'image_url', 'short_name')
