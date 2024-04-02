from venv import logger

from metrics.logic.celery_tasks import generate_report, report_cls_by_section_type
from metrics.models.report import SectionReport
from metrics.models.section_type import SectionType


def get_report(course_id: str, section_type: SectionType, should_generate_report: bool = False) -> SectionReport:
    if not should_generate_report:
        report = _get_existing_report(course_id, section_type)
        if report is not None:
            logger.info("Existing report found")
            return report

    return _create_empty_report(course_id, section_type)


def _get_existing_report(course_id: str, section_type: SectionType) -> SectionReport:
    return report_cls_by_section_type[section_type].objects.filter(course_id=course_id).first()


def _create_empty_report(course_id: str, section_type: SectionType) -> SectionReport:
    logger.info("Assigning task to generate report")
    generate_report.delay(course_id, section_type)
    return report_cls_by_section_type[section_type].objects.create(course_id=course_id)
