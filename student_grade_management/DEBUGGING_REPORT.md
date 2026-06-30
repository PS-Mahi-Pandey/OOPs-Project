# Debugging Report
## Student Grade Management System

---

## 1. Bug Description

An intentional bug was introduced in the `calculate_average()` method
inside the `Student` class (`buggy_version/models_buggy.py`).

The Python **integer division operator** `//` was used instead of the
correct **float division operator** `/` when computing the arithmetic
mean of a student's grades.

### Buggy Code (line 62 of `models_buggy.py`)

```python
# BUG: integer division truncates the decimal portion
return sum(self._grades.values()) // len(self._grades)   # ← BUG
```

### Fixed Code

```python
# CORRECT: float division preserves the decimal portion
return sum(self._grades.values()) / len(self._grades)    # ← FIX
```

---

## 2. Expected Result

The `calculate_average()` method should return the **exact arithmetic
mean** of all grades as a floating-point number, preserving the
decimal portion.

**Example:**

| Subject     | Score |
|-------------|-------|
| Mathematics | 85    |
| Physics     | 90    |
| Chemistry   | 78    |

Expected average = (85 + 90 + 78) / 3 = **84.3333…**

The report card should display:

```
  Average    :  84.33  (B)
```

---

## 3. Actual Result (with bug)

Because `//` performs **floor division** (integer division), the decimal
part is silently discarded:

```
(85 + 90 + 78) // 3  →  253 // 3  →  84   (not 84.33)
```

The report card displays:

```
  Average (BUGGY) : 84        ← wrong! decimal truncated
```

This also causes **wrong letter-grade assignments**. For example:

| Avg (correct) | Letter (correct) | Avg (buggy) | Letter (buggy) |
|---------------|-----------------|-------------|----------------|
| 87.5          | B+              | 87          | B              |
| 90.1          | A-              | 90          | A-  *(same)*   |
| 83.7          | B               | 83          | B-  *(wrong)*  |

For `GraduateStudent`, the bug propagates because
`GraduateStudent.calculate_average()` calls `super().calculate_average()`
which uses the buggy integer-division result before applying the
thesis weighting, compounding the inaccuracy.

---

## 4. Root Cause

Python has **two division operators**:

| Operator | Name             | Example        | Result |
|----------|-----------------|----------------|--------|
| `/`      | Float division   | `253 / 3`      | 84.333…|
| `//`     | Integer (floor) division | `253 // 3` | 84 |

The developer accidentally typed `//` (a common typo when the
programmer comes from languages where `/` between integers truncates).
Because Python 3 uses `float` for `/` by default, the correct operator
here is `/`. The `//` operator silently returns an `int`, which passes
all basic type checks, making the bug hard to spot without test cases
that check decimal precision.

---

## 5. Debugging Steps

### Step 1 – Reproduce the problem
Run `python buggy_version/demo_bug.py` to trigger the bug and observe
the incorrect average.

```
Expected average  : 84.3333
Buggy avg result  : 84
Difference        : 0.3333
Bug triggered?    : YES ✗
```

### Step 2 – Isolate the method
Add a quick diagnostic print inside `calculate_average()`:

```python
def calculate_average(self) -> float:
    if not self._grades:
        return 0.0
    total = sum(self._grades.values())
    count = len(self._grades)
    result = total // count         # BUG line
    print(f"[DEBUG] total={total}, count={count}, result={result}")
    return result
```

Output:
```
[DEBUG] total=253, count=3, result=84    ← truncated
```

### Step 3 – Compare operator behaviour
Open a Python REPL and test both operators:

```python
>>> 253 / 3
84.33333333333333   # correct
>>> 253 // 3
84                  # truncated – the bug
```

### Step 4 – Trace impact on letter-grade assignment
With `result = 84`, the `get_letter_grade()` loop finds the first
boundary where `84 >= boundary`. The boundary for `B-` is 80, and for
`B` it is 83, so grade `B` is assigned — one notch lower than the
correct `B+` (boundary 87, but 84.33 would map to `B`).

Actually for this specific example the letter-grade assignment is the
same (`B`), but for averages sitting right on a 0.5 boundary (e.g.
87.5 → `B+` but `87 // 1 = 87` → `B`) the bug causes a grade
**one step lower than deserved**.

### Step 5 – Confirm the fix
Change `//` to `/` and re-run:

```
Expected average  : 84.3333
Fixed avg result  : 84.3333
Difference        : 0.0000
Bug triggered?    : NO ✓
```

---

## 6. Screenshots / Console Output Evidence

Run the demo script to generate live evidence:

```bash
cd student_grade_management
python buggy_version/demo_bug.py
```

Expected console output:

```
============================================================
  BUG DEMONSTRATION: Integer Division in calculate_average()
============================================================

  Grades entered:
    Mathematics: 85
    Physics: 90
    Chemistry: 78

  Expected average  : 84.3333
  Buggy avg result  : 84
  Difference        : 0.3333
  Bug triggered?    : YES ✗

------------------------------------------------------------
  BUGGY Report Card output:
------------------------------------------------------------
================================================
  Student Report Card  [BUGGY VERSION]
================================================
  Name       : Test Student
  ID         : T001
  Mathematics          85.00  (B)
  Physics              90.00  (A-)
  Chemistry            78.00  (C+)
------------------------------------------------
  Average (BUGGY) : 84           ← truncated integer
================================================

------------------------------------------------------------
  FIXED Report Card output:
------------------------------------------------------------
================================================
  Student Report Card
================================================
  Name       : Test Student
  ID         : T001
  Type       : Undergraduate
------------------------------------------------
  Mathematics          85.00  (B)
  Physics              90.00  (A-)
  Chemistry            78.00  (C+)
------------------------------------------------
  Average    :  84.33  (B)       ← correct float
  Status     : PASS ✓
================================================
```

---

## 7. Final Fix

### File changed
`student_grade_management/models.py` — the production (fixed) version.

### Change applied

```python
# BEFORE (buggy)
return sum(self._grades.values()) // len(self._grades)

# AFTER (fixed)
return sum(self._grades.values()) / len(self._grades)
```

One character change (`//` → `/`) restores correct floating-point
division, ensuring the average is precise and letter-grade boundaries
are evaluated correctly.

The fix also indirectly corrects `GraduateStudent.calculate_average()`
which inherits the corrected base-class result.

---

*Report prepared by: Student — Student Grade Management System project*
