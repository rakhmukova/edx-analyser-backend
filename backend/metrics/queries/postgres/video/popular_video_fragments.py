from metrics.queries.postgres.sql_queries import SQL_QUERY_POPULAR_VIDEO_FRAGMENTS
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric
import pandas as pd
from matplotlib import pyplot as plt

def calc_play_video_count_daily(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_POPULAR_VIDEO_FRAGMENTS, (course_id, course_id, course_id,))

def popular_video_fragments():
    data = pd.read_csv("../../../../metric_results/DATSTPRO/video/popular_video_fragments.csv")

    video_counts = {}

    for index, row in data.iterrows():
        video_id = row['video_id']
        event_type = row['event_type']
        event_time = row['event_time']

        if video_id not in video_counts:
            video_counts[video_id] = {}

        if event_time not in video_counts[video_id]:
            video_counts[video_id][event_time] = 0

        if event_type == 'play_video':
            video_counts[video_id][event_time] += 1
        elif event_type == 'pause_video':
            video_counts[video_id][event_time] -= 1
    #
    # for video_id, counts in video_counts.items():
    #     print(f"Для видео {video_id}:")
    #     for event_time, count in counts.items():
    #         print(f"Время {event_time}: {count}")

    for video_id, counts in video_counts.items():
        times = list(counts.keys())
        views = list(counts.values())

        plt.figure(figsize=(10, 5))
        plt.plot(times, views, marker='o', linestyle='-')
        plt.title(f"График популярности видео {video_id}")
        plt.xlabel("Время")
        plt.ylabel("Количество просмотров")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


def main():
    # calc_course_metric(
    #     calc_play_video_count_daily,
    #     "video/popular_video_fragments.csv",
    #     ['video_id', 'event_type', 'event_time']
    # )
    popular_video_fragments()


if __name__ == '__main__':
    main()
