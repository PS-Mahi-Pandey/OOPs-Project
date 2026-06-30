# Student Grade Management System
A Python command-line application demonstrating core Object-Oriented Programming concepts.

## OOP Concepts Demonstrated

| Concept | Where |
|---|---|
| **Classes & Objects** | `Student`, `GraduateStudent`, `GradeManager` |
| **Encapsulation** | Private `_name`, `_grades`, `_student_id` with property getters/setters |
| **Abstraction** | `ReportGenerator` abstract base class (ABC) with `generate_report()` |
| **Inheritance** | `GraduateStudent` extends `Student`; both extend `ReportGenerator` |
| **Polymorphism** | Both classes override `calculate_average()` and `generate_report()` |
| **Functions** | `utils.py` helper functions, menu handler functions in `main.py` |

## Project Structure

```
student_grade_management/
├── main.py               ← Entry point / CLI menu
├── models.py             ← Student, GraduateStudent, ReportGenerator
├── manager.py            ← GradeManager (CRUD + statistics)
├── utils.py              ← Helper functions
├── buggy_version/
│   ├── models_buggy.py   ← Intentionally buggy version (// instead of /)
│   └── demo_bug.py       ← Script that shows bug vs fix side-by-side
├── DEBUGGING_REPORT.md   ← Full debugging report
└── README.md             ← This file
```

## How to Run

```bash
cd student_grade_management
python main.py
```

Demo data is pre-loaded (3 undergrad + 2 graduate students with grades).

## Run the Bug Demo

```bash
cd student_grade_management
python buggy_version/demo_bug.py
```

This prints a side-by-side comparison of the buggy vs correct average calculation.

## Requirements

- Python 3.10+ (uses `X | Y` union type hints)
- No external packages required
