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


class CourseManager(models.Manager):
    def available_courses(self, user_id: int):
        public_courses = Course.objects.filter(visibility=CourseVisibility.PUBLIC)
        user_courses = Course.objects.filter(owner=user_id)
        return public_courses | user_courses


class Course(models.Model):
    objects = CourseManager()

    course_id = models.CharField(max_length=MAX_COURSE_ID_LENGTH, null=False, blank=False)
    name = models.TextField(null=False, blank=False)
    image_url = models.TextField(null=True, blank=False)
    short_name = models.TextField(null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    visibility = models.CharField(choices=CourseVisibility.CHOICES, default=CourseVisibility.PRIVATE)

    class Meta:
        unique_together = ('owner', 'course_id')
