from rest_framework import serializers

from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'name', 'image_url', 'short_name']
