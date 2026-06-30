"""
manager.py
----------
GradeManager class – manages a collection of Student objects.
Demonstrates: Encapsulation, Functions/Methods, use of OOP composition.
"""

from models import Student, GraduateStudent


class GradeManager:
    """
    Central registry for all students.
    Provides CRUD operations and summary statistics.
    """

    def __init__(self):
        # Private dict keyed by student_id  →  Encapsulation
        self._students: dict[str, Student] = {}

    # ── Student CRUD ──────────────────────────
    def add_student(self, student: Student) -> bool:
        """Register a new student. Returns False if ID already exists."""
        if student.student_id in self._students:
            return False
        self._students[student.student_id] = student
        return True

    def remove_student(self, student_id: str) -> bool:
        """Remove a student by ID. Returns False if not found."""
        if student_id in self._students:
            del self._students[student_id]
            return True
        return False

    def get_student(self, student_id: str) -> Student | None:
        """Return the student object or None."""
        return self._students.get(student_id)

    def list_students(self) -> list[Student]:
        """Return all students sorted by name."""
        return sorted(self._students.values(), key=lambda s: s.name)

    def student_count(self) -> int:
        return len(self._students)

    # ── Grade operations ──────────────────────
    def add_grade(self, student_id: str, subject: str, score: float) -> bool:
        """Add/update a grade for a student. Returns False if student not found."""
        student = self.get_student(student_id)
        if student is None:
            return False
        student.add_grade(subject, score)
        return True

    # ── Statistics ────────────────────────────
    def class_average(self) -> float:
        """Return the mean average across all students who have grades."""
        students_with_grades = [s for s in self._students.values() if s.grades]
        if not students_with_grades:
            return 0.0
        return sum(s.calculate_average() for s in students_with_grades) / len(students_with_grades)

    def top_student(self) -> Student | None:
        """Return the student with the highest average."""
        students_with_grades = [s for s in self._students.values() if s.grades]
        if not students_with_grades:
            return None
        return max(students_with_grades, key=lambda s: s.calculate_average())

    def failing_students(self) -> list[Student]:
        """Return list of students who are currently failing."""
        return [s for s in self._students.values() if not s.is_passing() and s.grades]

    def passing_students(self) -> list[Student]:
        """Return list of students who are currently passing."""
        return [s for s in self._students.values() if s.is_passing() and s.grades]

    def subject_average(self, subject: str) -> float | None:
        """Return the class average for a specific subject, or None if no data."""
        scores = [s.grades[subject] for s in self._students.values()
                  if subject in s.grades]
        if not scores:
            return None
        return sum(scores) / len(scores)

    def summary_report(self) -> str:
        """Generate a text summary of the entire class."""
        lines = [
            "=" * 48,
            "  CLASS SUMMARY",
            "=" * 48,
            f"  Total Students : {self.student_count()}",
            f"  Class Average  : {self.class_average():.2f}",
            f"  Passing        : {len(self.passing_students())}",
            f"  Failing        : {len(self.failing_students())}",
        ]
        top = self.top_student()
        if top:
            lines.append(f"  Top Student    : {top.name}  ({top.calculate_average():.2f})")
        lines.append("=" * 48)
        return "\n".join(lines)
