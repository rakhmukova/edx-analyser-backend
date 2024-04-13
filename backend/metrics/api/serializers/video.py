from rest_framework import serializers

from metrics.models.video import VideoPlayCountChart, VideoInteractionChart, VideoInteraction, VideoPlayCount


class VideoPlayCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPlayCount
        fields = ['date', 'count']

class VideoInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoInteraction
        fields = ['video_link', 'views_count', 'unique_students_count']

    # more effective way of passing data
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     print(data)
    #     values_list = [data[field] for field in self.Meta.fields]
    #     return values_list


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
