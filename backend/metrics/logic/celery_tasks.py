from datetime import datetime
from typing import Type
from venv import logger

from app.celery import app
from metrics.models.common import CompletionDegreeChart, SessionTimeChart, SectionActivityChart
from metrics.models.report import VideoSectionReport, CommonSectionReport, SectionReport
from metrics.models.section_type import SectionType
from metrics.models.video import VideoInteractionChart, VideoPlayCountChart, VideoPlayCount, VideoInteraction


def _create_common_section_report(course_id: str):
    completion_degree_chart = CompletionDegreeChart.objects.create()
    session_time_chart = SessionTimeChart.objects.create()
    section_activity_chart = SectionActivityChart.objects.create()
    report = CommonSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.completion_degree_chart = completion_degree_chart
    report.session_time_chart = session_time_chart
    report.section_activity_chart = section_activity_chart
    report.save()


def _create_video_section_report(course_id: str):
    video_play_count_chart = VideoPlayCountChart.objects.create()
    VideoPlayCount.objects.create(
        date=datetime.now(),
        count=1,
        chart=video_play_count_chart
    )
    video_interaction_chart = VideoInteractionChart.objects.create()
    VideoInteraction.objects.create(
        video_link="video_link",
        students_visits_count=1,
        viewing_percent_median=1,
        chart=video_interaction_chart
    )
    report = VideoSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.video_play_count_chart = video_play_count_chart
    report.video_interaction_chart = video_interaction_chart
    report.save()

create_func_by_section_type = {
    SectionType.COMMON: _create_common_section_report,
    SectionType.VIDEO: _create_video_section_report
}

report_cls_by_section_type: dict[SectionType, Type[SectionReport]] = {
    SectionType.VIDEO: VideoSectionReport,
    SectionType.COMMON: CommonSectionReport
}

@app.task(name="generate_report")
def generate_report(course_id: str, section_type: SectionType):
    try:
        logger.info(f"Generating report for section {section_type}")
        create_report(course_id, section_type)
    except Exception as e:
        # can have this error as well
        logger.error("Ошибка при создании отчета:", e)
        report = report_cls_by_section_type[section_type].objects.filter(
            course_id = course_id
        ).first()
        # handle error
        report.error_reason = str(e)
        report.save()


# potentially long operation - need to calc metrics and save them
def create_report(course_id: str, section_type: SectionType) -> None:
    create_func_by_section_type[section_type](course_id)
