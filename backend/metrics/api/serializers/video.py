from rest_framework import serializers

from metrics.models.video import VideoPlayCountChart, VideoInteractionChart, VideoInteraction, VideoPlayCount


class VideoPlayCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPlayCount
        fields = ['date', 'count']

class VideoInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoInteraction
        fields = ['video_link', 'students_visits_count', 'viewing_percent_median']


class VideoPlayCountChartSerializer(serializers.ModelSerializer):
    items = VideoPlayCountSerializer(many=True)
    class Meta:
        model = VideoPlayCountChart
        fields = ['items']

class VideoInteractionChartSerializer(serializers.ModelSerializer):
    items = VideoInteractionSerializer(many=True)
    class Meta:
        model = VideoInteractionChart
        fields = ['items']
