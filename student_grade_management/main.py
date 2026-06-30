"""
main.py
-------
Entry point for the Student Grade Management System.
Provides a menu-driven CLI that exercises all OOP features.

Run:
    python main.py
"""

import sys
import os

# Allow running from the project folder directly
sys.path.insert(0, os.path.dirname(__file__))

from models import Student, GraduateStudent
from manager import GradeManager
from utils import (
    get_float_input,
    get_non_empty_input,
    get_menu_choice,
    format_score_bar,
    print_header,
    clear_screen,
)


# ─────────────────────────────────────────────
#  Menu handler functions
# ─────────────────────────────────────────────

def menu_add_student(mgr: GradeManager) -> None:
    print_header("Add New Student")
    s_type = get_menu_choice(
        "  Student type – (1) Undergraduate  (2) Graduate: ",
        ["1", "2"],
    )
    name = get_non_empty_input("  Full name       : ")
    sid  = get_non_empty_input("  Student ID      : ")

    if mgr.get_student(sid):
        print(f"\n  ⚠  A student with ID '{sid}' already exists.")
        return

    if s_type == "1":
        student = Student(name, sid)
    else:
        advisor = get_non_empty_input("  Advisor name    : ")
        thesis  = get_non_empty_input("  Thesis title    : ")
        student = GraduateStudent(name, sid, advisor, thesis)

    mgr.add_student(student)
    print(f"\n  ✔  {student} added successfully.")


def menu_view_students(mgr: GradeManager) -> None:
    print_header("All Students")
    students = mgr.list_students()
    if not students:
        print("  No details entered yet.")
        return

    print(f"  {'#':<4} {'Name':<22} {'ID':<12} {'Type':<14} {'Avg':>6}  {'Status'}")
    print("  " + "-" * 64)
    for i, s in enumerate(students, 1):
        s_type = "Graduate" if isinstance(s, GraduateStudent) else "Undergraduate"
        avg    = s.calculate_average()
        status = "PASS" if s.is_passing() else ("FAIL" if s.grades else "-")
        print(f"  {i:<4} {s.name:<22} {s.student_id:<12} {s_type:<14} {avg:>6.2f}  {status}")


def menu_add_grade(mgr: GradeManager) -> None:
    print_header("Add / Update Grade")
    sid = get_non_empty_input("  Student ID : ")
    student = mgr.get_student(sid)
    if student is None:
        print(f"  ⚠  No student found with ID '{sid}'.")
        return

    subject = get_non_empty_input(f"  Subject for {student.name}: ")
    score   = get_float_input("  Score (0-100)  : ")
    student.add_grade(subject, score)
    letter = student.get_letter_grade(score)
    print(f"\n  ✔  {subject}: {score:.2f} ({letter}) recorded for {student.name}.")

    # For graduate students, offer to record thesis score
    if isinstance(student, GraduateStudent):
        add_thesis = get_menu_choice("  Record thesis score? (y/n): ", ["y", "n"])
        if add_thesis == "y":
            t_score = get_float_input("  Thesis score (0-100): ")
            student.set_thesis_score(t_score)
            print(f"  ✔  Thesis score {t_score:.2f} recorded.")


def menu_view_report(mgr: GradeManager) -> None:
    print_header("Student Report Card")
    sid = get_non_empty_input("  Student ID : ")
    student = mgr.get_student(sid)
    if student is None:
        print(f"  ⚠  No student found with ID '{sid}'.")
        return
    print()
    student.print_report()   # uses the abstract method defined in ReportGenerator

    # Show visual score bars
    if student.grades:
        print("\n  Score Breakdown:")
        for subj, score in student.grades.items():
            print(f"  {subj:<20} {format_score_bar(score)}")


def menu_remove_student(mgr: GradeManager) -> None:
    print_header("Remove Student")
    sid = get_non_empty_input("  Student ID to remove: ")
    student = mgr.get_student(sid)
    if student is None:
        print(f"  ⚠  No student found with ID '{sid}'.")
        return
    confirm = get_menu_choice(
        f"  Remove {student.name}? This cannot be undone. (y/n): ",
        ["y", "n"],
    )
    if confirm == "y":
        mgr.remove_student(sid)
        print(f"  ✔  {student.name} removed.")
    else:
        print("  Cancelled.")


def menu_class_summary(mgr: GradeManager) -> None:
    print_header("Class Summary")
    print(mgr.summary_report())

    failing = mgr.failing_students()
    if failing:
        print("\n  ⚠  Failing students:")
        for s in failing:
            print(f"     • {s.name}  ({s.student_id})  avg={s.calculate_average():.2f}")


def menu_subject_average(mgr: GradeManager) -> None:
    print_header("Subject Average")
    subject = get_non_empty_input("  Subject name: ")
    avg = mgr.subject_average(subject)
    if avg is None:
        print(f"  ⚠  No grades found for '{subject}'.")
    else:
        print(f"\n  Class average for '{subject}': {avg:.2f}  ({format_score_bar(avg)})")


def menu_search_student(mgr: GradeManager) -> None:
    print_header("Search Student")
    query = get_non_empty_input("  Enter name or ID to search: ").lower()
    results = [
        s for s in mgr.list_students()
        if query in s.name.lower() or query in s.student_id.lower()
    ]
    if not results:
        print("  No matching students found.")
    else:
        print(f"  Found {len(results)} result(s):")
        for s in results:
            s_type = "Graduate" if isinstance(s, GraduateStudent) else "Undergraduate"
            print(f"    • {s.name}  (ID: {s.student_id})  [{s_type}]")





# ─────────────────────────────────────────────
#  Main application loop
# ─────────────────────────────────────────────

MENU = """
  ╔══════════════════════════════════════════╗
  ║   STUDENT GRADE MANAGEMENT SYSTEM        ║
  ╠══════════════════════════════════════════╣
  ║  1. View All Students                    ║
  ║  2. Add New Student                      ║
  ║  3. Add / Update Grade                   ║
  ║  4. View Student Report Card             ║
  ║  5. Search Student                       ║
  ║  6. Remove Student                       ║
  ║  0. Exit                                 ║
  ╚══════════════════════════════════════════╝
"""

MENU_HANDLERS = {
    "1": menu_view_students,
    "2": menu_add_student,
    "3": menu_add_grade,
    "4": menu_view_report,
    "5": menu_search_student,
    "6": menu_remove_student,
}


def main() -> None:
    mgr = GradeManager()

    print("\n  Welcome to the Student Grade Management System!")
    print("  No students yet. Use the menu to add students.")

    while True:
        print(MENU)
        choice = input("  Enter your choice: ").strip()

        if choice == "0":
            print("\n  Goodbye!\n")
            break
        elif choice in MENU_HANDLERS:
            try:
                MENU_HANDLERS[choice](mgr)
            except Exception as exc:
                print(f"\n  ✖  Unexpected error: {exc}")
        else:
            print("  ⚠  Invalid choice. Please enter a number from the menu.")

        input("\n  Press Enter to continue...")
        clear_screen()


if __name__ == "__main__":
    main()
