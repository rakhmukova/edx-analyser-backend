from django.db import models

from metrics.models.util import MAX_COURSE_ID_LENGTH


# key in postgres - course_id + section_name or smth
class CourseReport(models.Model):
    course_id = models.CharField(max_length=MAX_COURSE_ID_LENGTH)
    last_time_accessed = models.DateTimeField()
    last_time_updated = models.DateTimeField()

    class Meta:
        abstract = True


class VideoSectionReport(CourseReport):
    pass


class CommonSectionReport(CourseReport):
    pass
