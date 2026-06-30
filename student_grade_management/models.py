"""
models.py
---------
Core data models for the Student Grade Management System.
Demonstrates: Classes, Objects, Encapsulation, Inheritance, Polymorphism, Abstraction
"""

from abc import ABC, abstractmethod


# ─────────────────────────────────────────────
#  ABSTRACTION  –  Abstract base for reporters
# ─────────────────────────────────────────────
class ReportGenerator(ABC):
    """Abstract base class that forces every concrete reporter
    to implement generate_report()."""

    @abstractmethod
    def generate_report(self) -> str:
        """Return a formatted report string."""
        pass

    def print_report(self) -> None:
        """Template method: print the report to stdout."""
        print(self.generate_report())


# ─────────────────────────────────────────────
#  ENCAPSULATION  –  Student class
# ─────────────────────────────────────────────
class Student(ReportGenerator):
    """
    Represents an undergraduate student.

    Private attributes (_name, _student_id, _grades) are accessed
    only through property getters / setters – demonstrating Encapsulation.
    """

    # Grade boundaries (class-level constant)
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
        self._grades: dict[str, float] = {}   # {subject: score}

    # ── Properties (getters) ──────────────────
    @property
    def name(self) -> str:
        return self._name

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def grades(self) -> dict:
        """Return a copy so the caller cannot mutate internal state."""
        return dict(self._grades)

    # ── Setters with validation ───────────────
    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    # ── Grade management methods ──────────────
    def add_grade(self, subject: str, score: float) -> None:
        """Add or update a grade for a subject."""
        if not (0 <= score <= 100):
            raise ValueError(f"Score must be between 0 and 100, got {score}.")
        self._grades[subject.strip()] = score

    def remove_grade(self, subject: str) -> bool:
        """Remove a subject grade. Returns True if removed, False if not found."""
        if subject in self._grades:
            del self._grades[subject]
            return True
        return False

    def calculate_average(self) -> float:
        """Return the arithmetic mean of all grades."""
        if not self._grades:
            return 0.0
        return sum(self._grades.values()) / len(self._grades)

    def get_letter_grade(self, score: float | None = None) -> str:
        """Convert a numeric score (or the average) to a letter grade."""
        value = score if score is not None else self.calculate_average()
        for letter, boundary in self.GRADE_BOUNDARIES.items():
            if value >= boundary:
                return letter
        return "F"

    def is_passing(self) -> bool:
        """Return True if the student's average is >= 60."""
        return self.calculate_average() >= 60

    # ── Polymorphism – overrides abstract method ──
    def generate_report(self) -> str:
        avg = self.calculate_average()
        lines = [
            "=" * 48,
            f"  Student Report Card",
            "=" * 48,
            f"  Name       : {self._name}",
            f"  ID         : {self._student_id}",
            f"  Type       : Undergraduate",
            "-" * 48,
        ]
        if self._grades:
            for subject, score in self._grades.items():
                letter = self.get_letter_grade(score)
                lines.append(f"  {subject:<20} {score:>6.2f}  ({letter})")
            lines.append("-" * 48)
            lines.append(f"  Average    : {avg:>6.2f}  ({self.get_letter_grade()})")
            lines.append(f"  Status     : {'PASS ✓' if self.is_passing() else 'FAIL ✗'}")
        else:
            lines.append("  No grades recorded.")
        lines.append("=" * 48)
        return "\n".join(lines)

    def __str__(self) -> str:
        return f"Student({self._name}, ID={self._student_id})"

    def __repr__(self) -> str:
        return self.__str__()


# ─────────────────────────────────────────────
#  INHERITANCE + POLYMORPHISM – Graduate student
# ─────────────────────────────────────────────
class GraduateStudent(Student):
    """
    Extends Student with a thesis score and advisor information.
    Overrides calculate_average() and generate_report() – Polymorphism.
    """

    THESIS_WEIGHT = 0.30   # thesis counts 30 % of overall average

    def __init__(self, name: str, student_id: str, advisor: str, thesis_title: str):
        super().__init__(name, student_id)
        self._advisor = advisor
        self._thesis_title = thesis_title
        self._thesis_score: float | None = None

    # ── Extra properties ──────────────────────
    @property
    def advisor(self) -> str:
        return self._advisor

    @property
    def thesis_title(self) -> str:
        return self._thesis_title

    @property
    def thesis_score(self) -> float | None:
        return self._thesis_score

    def set_thesis_score(self, score: float) -> None:
        if not (0 <= score <= 100):
            raise ValueError(f"Thesis score must be 0-100, got {score}.")
        self._thesis_score = score

    # ── Polymorphism – override average ───────
    def calculate_average(self) -> float:
        """
        Weighted average: 70 % coursework + 30 % thesis (if thesis scored).
        Falls back to plain average when no thesis score is set.
        """
        course_avg = super().calculate_average()
        if self._thesis_score is None:
            return course_avg
        return (course_avg * (1 - self.THESIS_WEIGHT) +
                self._thesis_score * self.THESIS_WEIGHT)

    # ── Polymorphism – override report ────────
    def generate_report(self) -> str:
        avg = self.calculate_average()
        lines = [
            "=" * 48,
            f"  Graduate Student Report Card",
            "=" * 48,
            f"  Name       : {self._name}",
            f"  ID         : {self._student_id}",
            f"  Type       : Graduate",
            f"  Advisor    : {self._advisor}",
            f"  Thesis     : {self._thesis_title}",
            "-" * 48,
        ]
        if self._grades:
            for subject, score in self._grades.items():
                letter = self.get_letter_grade(score)
                lines.append(f"  {subject:<20} {score:>6.2f}  ({letter})")
        else:
            lines.append("  No coursework grades recorded.")

        lines.append("-" * 48)
        thesis_display = (f"{self._thesis_score:.2f}  ({self.get_letter_grade(self._thesis_score)})"
                          if self._thesis_score is not None else "Not graded yet")
        lines.append(f"  Thesis Score : {thesis_display}")
        lines.append(f"  Overall Avg  : {avg:>6.2f}  ({self.get_letter_grade()})")
        lines.append(f"  Status       : {'PASS ✓' if self.is_passing() else 'FAIL ✗'}")
        lines.append("=" * 48)
        return "\n".join(lines)

    def __str__(self) -> str:
        return f"GraduateStudent({self._name}, ID={self._student_id})"
