"""
demo_bug.py
-----------
Demonstrates the bug and the fix side-by-side so it can be
run to produce evidence for the Debugging Report.

Run:
    python buggy_version/demo_bug.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from buggy_version.models_buggy import Student as BuggyStudent
from models import Student as FixedStudent


def run_comparison():
    print("=" * 60)
    print("  BUG DEMONSTRATION: Integer Division in calculate_average()")
    print("=" * 60)

    grades = {
        "Mathematics": 85,
        "Physics":     90,
        "Chemistry":   78,
    }
    # Correct average: (85 + 90 + 78) / 3 = 84.333...

    buggy = BuggyStudent("Test Student", "T001")
    fixed = FixedStudent("Test Student", "T001")

    for subj, score in grades.items():
        buggy.add_grade(subj, score)
        fixed.add_grade(subj, score)

    buggy_avg = buggy.calculate_average()
    fixed_avg = fixed.calculate_average()

    print(f"\n  Grades entered:")
    for subj, score in grades.items():
        print(f"    {subj}: {score}")

    print(f"\n  Expected average  : {fixed_avg:.4f}")
    print(f"  Buggy avg result  : {buggy_avg}")
    print(f"\n  Difference        : {abs(fixed_avg - buggy_avg):.4f}")
    print(f"  Bug triggered?    : {'YES ✗' if buggy_avg != fixed_avg else 'NO ✓'}")

    print("\n" + "-" * 60)
    print("  BUGGY Report Card output:")
    print("-" * 60)
    buggy.print_report()

    print("\n" + "-" * 60)
    print("  FIXED Report Card output:")
    print("-" * 60)
    fixed.print_report()


if __name__ == "__main__":
    run_comparison()
