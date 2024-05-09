from django.contrib.auth.models import User
from django.db import models

MAX_COURSE_ID_LENGTH = 150


class CourseVisibility:
    PUBLIC = "Public"
    PRIVATE = "Private"

    CHOICES = (
        (PUBLIC, "Public"),
        (PRIVATE, "Private")
    )


class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=MAX_COURSE_ID_LENGTH, null=False, blank=False)
    name = models.TextField(null=False, blank=False)
    image_url = models.TextField(null=True, blank=False)
    short_name = models.TextField(null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    visibility = models.CharField(choices=CourseVisibility.CHOICES, default=CourseVisibility.PRIVATE)
