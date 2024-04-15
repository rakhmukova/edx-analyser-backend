from typing import Type
from venv import logger

from app.celery import app
from metrics.logic.celery_tasks.common import \
    create_section_activity_chart, create_weekly_activity_chart
from metrics.logic.celery_tasks.forum import create_forum_question_chart
from metrics.logic.celery_tasks.pages import create_pages_popularity_chart
from metrics.logic.celery_tasks.tasks import create_task_complexity_chart, create_task_summary_chart
from metrics.logic.celery_tasks.textbook import create_word_search_chart
from metrics.logic.celery_tasks.video import create_video_interaction_chart, create_video_play_count_chart
from metrics.models.report import VideoSectionReport, CommonSectionReport, SectionReport, PagesSectionReport, \
    TaskSectionReport, TextbookSectionReport, ForumSectionReport
from metrics.models.section_type import SectionType

report_cls_by_section_type: dict[SectionType, Type[SectionReport]] = {
    SectionType.VIDEO: VideoSectionReport,
    SectionType.COMMON: CommonSectionReport,
    SectionType.PAGES: PagesSectionReport,
    SectionType.TASKS: TaskSectionReport,
    SectionType.PDF: TextbookSectionReport,
    SectionType.FORUM: ForumSectionReport
}


def _create_common_section_report(course_id: str):
    section_activity_chart = create_section_activity_chart(course_id)
    weekly_activity_chart = create_weekly_activity_chart(course_id)
    students_count = 125
    active_students_count = 120
    report = CommonSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.section_activity_chart = section_activity_chart
    report.weekly_activity_chart = weekly_activity_chart
    report.students_count = students_count
    report.active_students_count = active_students_count
    report.save()


def _create_video_section_report(course_id: str):
    video_play_count_chart = create_video_play_count_chart(course_id)
    video_interaction_chart = create_video_interaction_chart(course_id)
    report = VideoSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.video_play_count_chart = video_play_count_chart
    report.video_interaction_chart = video_interaction_chart
    report.save()


def _create_page_section_report(course_id: str):
    pages_popularity_chart = create_pages_popularity_chart(course_id)
    report = PagesSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.pages_popularity_chart = pages_popularity_chart
    report.save()


def _create_textbook_section_report(course_id: str):
    # textbook_views_chart = create_textbook_views_chart(course_id)
    word_search_chart = create_word_search_chart(course_id)
    report = TextbookSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.word_search_chart = word_search_chart
    report.save()


def _create_forum_section_report(course_id: str):
    forum_question_chart = create_forum_question_chart(course_id)
    report = ForumSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.forum_question_chart = forum_question_chart
    report.save()

def _create_task_section_report(course_id: str):
    task_complexity_chart = create_task_complexity_chart(course_id)
    task_summary_chart = create_task_summary_chart(course_id)
    report = TaskSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.task_complexity_chart = task_complexity_chart
    report.task_summary_chart = task_summary_chart
    report.save()


create_func_by_section_type = {
    SectionType.COMMON: _create_common_section_report,
    SectionType.VIDEO: _create_video_section_report,
    SectionType.PAGES: _create_page_section_report,
    SectionType.PDF: _create_textbook_section_report,
    SectionType.TASKS: _create_task_section_report,
    SectionType.FORUM: _create_forum_section_report
}


# potentially long operation - need to calc metrics and save them
def _create_report(course_id: str, section_type: SectionType) -> None:
    create_func_by_section_type[section_type](course_id)


@app.task(name="generate_report")
def generate_report(course_id: str, section_type: SectionType):
    try:
        logger.info(f"Generating report for section {section_type}")
        _create_report(course_id, section_type)
    except Exception as e:
        # can have this error as well
        logger.error("Ошибка при создании отчета:", e)
        report = report_cls_by_section_type[section_type].objects.filter(
            course_id=course_id
        ).first()
        # handle error
        # value too long for type character varying(100)
        # report.error_reason = str(e)
        report.save()
