from datetime import datetime

from metrics.models.report import CourseReport, CommonSectionReport, VideoSectionReport
from metrics.models.report_state import ReportState
from metrics.models.section_type import SectionType


class ReportManager:

    @staticmethod
    def get_report(course_id: str, section_type: SectionType, should_create_new=False) -> CourseReport:
        # todo: get rid of if else here
        if section_type == SectionType.COMMON:
            return CommonSectionReport.objects.create(
                course_id=course_id,
                last_time_accessed=datetime.now(),
                last_time_updated=datetime.now(),
                report_state=ReportState.CREATED
            )
        elif section_type == SectionType.VIDEO:
            return VideoSectionReport.objects.create(
                course_id=course_id,
                last_time_accessed=datetime.now(),
                last_time_updated=datetime.now(),
                report_state=ReportState.FAILED
            )
