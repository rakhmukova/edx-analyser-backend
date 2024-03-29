from datetime import datetime

from metrics.models.report import CourseReport, CommonSectionReport, VideoSectionReport
from metrics.models.section_type import SectionType


class ReportManager:

    @staticmethod
    def generate_report(course_id: str, section_type: SectionType) -> CourseReport:
#         get rid of if
        if section_type == SectionType.COMMON:
            return CommonSectionReport.objects.create(
                course_id=course_id,
                last_time_accessed=datetime.now(),
                last_time_updated=datetime.now()
            )
        elif section_type == SectionType.VIDEO:
            return VideoSectionReport.objects.create(
                course_id=course_id,
                last_time_accessed=datetime.now(),
                last_time_updated=datetime.now()
            )
