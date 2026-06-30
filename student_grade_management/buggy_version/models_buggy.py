"""
models_buggy.py
---------------
>>> INTENTIONAL BUG VERSION <<<

BUG INTRODUCED:
    In the calculate_average() method of the Student class,
    the denominator uses len(self._grades.keys()) but the
    sum uses self._grades.values() — however the real bug is
    that the division is done with integer division (//) instead
    of float division (/), causing truncated (wrong) averages.

    Example:
        Grades: Math=85, Physics=90  →  correct avg = 87.5
        Bug result: 85 + 90 = 175 // 2 = 87   ← truncated!
"""

from abc import ABC, abstractmethod


class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(self) -> str:
        pass

    def print_report(self) -> None:
        print(self.generate_report())


class Student(ReportGenerator):
    GRADE_BOUNDARIES = {
        "A+": 97, "A": 93, "A-": 90,
        "B+": 87, "B": 83, "B-": 80,
        "C+": 77, "C": 73, "C-": 70,
        "D+": 67, "D": 60,
        "F":  0,
    }

    def __init__(self, name: str, student_id: str):
        self._name = name
        self._student_id = student_id
        self._grades: dict = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def grades(self) -> dict:
        return dict(self._grades)

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    def add_grade(self, subject: str, score: float) -> None:
        if not (0 <= score <= 100):
            raise ValueError(f"Score must be between 0 and 100, got {score}.")
        self._grades[subject.strip()] = score

    def remove_grade(self, subject: str) -> bool:
        if subject in self._grades:
            del self._grades[subject]
            return True
        return False

    def calculate_average(self) -> float:
        """
        ╔══════════════════════════════════════════════╗
        ║  ★  INTENTIONAL BUG IS HERE  ★               ║
        ║                                              ║
        ║  Using integer division operator (//)        ║
        ║  instead of float division (/).              ║
        ║  This truncates the decimal part of the avg. ║
        ╚══════════════════════════════════════════════╝
        """
        if not self._grades:
            return 0.0
        # BUG: should be  /  not  //
        return sum(self._grades.values()) // len(self._grades)   # ← BUG LINE

    def get_letter_grade(self, score=None) -> str:
        value = score if score is not None else self.calculate_average()
        for letter, boundary in self.GRADE_BOUNDARIES.items():
            if value >= boundary:
                return letter
        return "F"

    def is_passing(self) -> bool:
        return self.calculate_average() >= 60

    def generate_report(self) -> str:
        avg = self.calculate_average()
        lines = [
            "=" * 48,
            "  Student Report Card  [BUGGY VERSION]",
            "=" * 48,
            f"  Name       : {self._name}",
            f"  ID         : {self._student_id}",
        ]
        if self._grades:
            for subject, score in self._grades.items():
                letter = self.get_letter_grade(score)
                lines.append(f"  {subject:<20} {score:>6.2f}  ({letter})")
            lines.append("-" * 48)
            lines.append(f"  Average (BUGGY) : {avg}")
        else:
            lines.append("  No grades recorded.")
        lines.append("=" * 48)
        return "\n".join(lines)

    def __str__(self) -> str:
        return f"Student({self._name}, ID={self._student_id})"


class GraduateStudent(Student):
    THESIS_WEIGHT = 0.30

    def __init__(self, name, student_id, advisor, thesis_title):
        super().__init__(name, student_id)
        self._advisor = advisor
        self._thesis_title = thesis_title
        self._thesis_score = None

    @property
    def advisor(self):
        return self._advisor

    @property
    def thesis_title(self):
        return self._thesis_title

    def set_thesis_score(self, score: float) -> None:
        if not (0 <= score <= 100):
            raise ValueError(f"Thesis score must be 0-100, got {score}.")
        self._thesis_score = score

    def calculate_average(self) -> float:
        course_avg = super().calculate_average()   # inherits the bug
        if self._thesis_score is None:
            return course_avg
        return (course_avg * (1 - self.THESIS_WEIGHT) +
                self._thesis_score * self.THESIS_WEIGHT)

    def generate_report(self) -> str:
        avg = self.calculate_average()
        lines = [
            "=" * 48,
            "  Graduate Student Report  [BUGGY VERSION]",
            "=" * 48,
            f"  Name    : {self._name}",
            f"  ID      : {self._student_id}",
            f"  Advisor : {self._advisor}",
        ]
        for subject, score in self._grades.items():
            lines.append(f"  {subject:<20} {score:>6.2f}")
        lines.append(f"  Average (BUGGY) : {avg}")
        lines.append("=" * 48)
        return "\n".join(lines)
