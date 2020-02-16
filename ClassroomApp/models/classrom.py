from dataclasses import dataclass, field
from typing import List

from models.student import Student
from models.teacher import Teacher


@dataclass
class Classroom:
    teacher: Teacher
    students: List[Student] = field(default_factory=list)  # avoiding default mutable list

    def __post_init__(self):
        if not self.teacher:
            raise ValueError("Teacher field cannot be empty")
