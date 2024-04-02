from datetime import datetime

from metrics.models.video import VideoInteractionChart, VideoInteraction, VideoPlayCountChart, VideoPlayCount
from metrics.utils.file_operations import csv_to_json


def create_video_interaction_chart(course_id: str) -> VideoInteractionChart:
    video_interaction_chart = VideoInteractionChart.objects.create()
    VideoInteraction.objects.create(
        video_link="some video",
        students_visits_count=1,
        viewing_percent_median=1,
        chart=video_interaction_chart
    )
    VideoInteraction.objects.create(
        video_link="another video",
        students_visits_count=2,
        viewing_percent_median=2,
        chart=video_interaction_chart
    )
    return video_interaction_chart


def create_video_play_count_chart(course_id: str) -> VideoPlayCountChart:
    video_play_count_chart = VideoPlayCountChart.objects.create()
    chart_objects_json = csv_to_json(
        'metric_results/existing/play_video_count_daily.csv',
        {
            'date': datetime,
            'count': int
        })

    models = [VideoPlayCount(**item, chart=video_play_count_chart) for item in chart_objects_json]
    VideoPlayCount.objects.bulk_create(models)
    return video_play_count_chart
