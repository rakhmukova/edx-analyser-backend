from datetime import datetime

from metrics.logic.celery_tasks.util import bulk_create_from_csv
from metrics.models.video import VideoInteractionChart, VideoInteraction, VideoPlayCountChart, VideoPlayCount


def create_video_interaction_chart(course_id: str) -> VideoInteractionChart:
    return bulk_create_from_csv(
        'metric_results/existing/video/video_popularity.csv',
        {
            'video_link': str,
            'views_count': int,
            'unique_students_count': int
        },
        VideoInteraction,
        VideoInteractionChart
    )


def create_video_play_count_chart(course_id: str) -> VideoPlayCountChart:
    # result = calc_course_metric(
    #     calc_play_video_count_daily,
    #     'play_video_count_daily.csv',
    #     ['date', 'count']
    # )
    # print(result)
    return bulk_create_from_csv(
        'metric_results/existing/video/play_video_count_daily.csv',
        {
            'date': datetime,
            'count': int
        },
        VideoPlayCount,
        VideoPlayCountChart
    )
