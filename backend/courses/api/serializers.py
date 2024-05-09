from rest_framework import serializers

from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(
        source="owner.username", read_only=True)

    class Meta:
        model = Course
        fields = ['course_id', 'name', 'image_url', 'owner', 'visibility']
