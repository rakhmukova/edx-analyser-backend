from django.db import models

MAX_COURSE_ID_LENGTH = 150


class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=MAX_COURSE_ID_LENGTH, null=False, blank=False)
    name = models.TextField(null=False, blank=False)
    image_url = models.TextField(null=True, blank=False)
    short_name = models.TextField(null=False, blank=False)
