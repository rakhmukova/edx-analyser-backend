from datetime import datetime

from metrics.logic.celery_tasks.util import bulk_create_from_csv
from metrics.models.video import VideoInteractionChart, VideoInteraction, VideoPlayCountChart, VideoPlayCount
from metrics.queries.postgres.video.play_video_count_daily import calc_play_video_count_daily
from metrics.utils.metric_operations import calc_course_metric


def create_video_interaction_chart(course_id: str) -> VideoInteractionChart:
    video_interaction_chart = VideoInteractionChart.objects.create()
    VideoInteraction.objects.create(
        video_link="some video",
        views_count=1,
        unique_students_count=1,
        chart=video_interaction_chart
    )
    VideoInteraction.objects.create(
        video_link="another video",
        views_count=2,
        unique_students_count=2,
        chart=video_interaction_chart
    )
    return video_interaction_chart


def create_video_play_count_chart(course_id: str) -> VideoPlayCountChart:
    result = calc_course_metric(
        calc_play_video_count_daily,
        'play_video_count_daily.csv',
        ['date', 'count']
    )
    print(result)
    return bulk_create_from_csv(
        'metric_results/existing/play_video_count_daily.csv',
        {
            'date': datetime,
            'count': int
        },
        VideoPlayCount,
        VideoPlayCountChart
    )
