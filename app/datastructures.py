from typing import NamedTuple


class CourseCapacityReport(NamedTuple):
    capacity: int
    available_seats: int
