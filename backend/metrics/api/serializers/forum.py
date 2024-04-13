from rest_framework import serializers

from metrics.models.forum import ForumQuestionChart, ForumQuestion


class ForumQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumQuestion
        fields = ['author', 'title', 'body', 'likes_count', 'comments_count', 'question_type']


class ForumQuestionChartSerializer(serializers.ModelSerializer):
    items = ForumQuestionSerializer(many=True)

    class Meta:
        model = ForumQuestionChart
        fields = ['items']