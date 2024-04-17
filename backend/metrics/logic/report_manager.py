from venv import logger

from metrics.logic.celery_tasks.generate_report import generate_report, report_cls_by_section_type
from metrics.models.report import SectionReport
from metrics.models.section_type import SectionType


def get_report(course_id: str, section_type: SectionType, force_update: bool = False) -> SectionReport:
    # todo: check course_id is in available courses
    if not force_update:
        report = _get_existing_report(course_id, section_type)
        if report is not None:
            logger.info("Existing report found")
            return report

    report = _create_empty_report(course_id, section_type)
    generate_report.delay(course_id, section_type)
    return report


def _get_existing_report(course_id: str, section_type: SectionType) -> SectionReport:
    return report_cls_by_section_type[section_type].objects.filter(course_id=course_id).first()


def _create_empty_report(course_id: str, section_type: SectionType) -> SectionReport:
    logger.info("Assigning task to generate report")
    return report_cls_by_section_type[section_type].objects.create(course_id=course_id)
