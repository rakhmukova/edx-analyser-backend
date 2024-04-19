from metrics.logic.celery_tasks.util import bulk_create_from_csv
from metrics.models.forum import ForumQuestion, ForumQuestionChart


def create_forum_question_chart(course_id: str) -> ForumQuestionChart:
    return bulk_create_from_csv(
        f'metric_results/{course_id}/forum/top_questions.csv',
        {
            'author': str,
            'title': str,
            'body': str,
            'likes_count': str,
            'comments_count': str,
            'question_type': str
        },
        ForumQuestion,
        ForumQuestionChart
    )
