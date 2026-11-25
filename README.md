# Student Fee Management System

**PS No. 64 — Bachelor of Computer Application**  
**Language:** Python 3  
**Concepts:** Dictionaries, Functions, Conditions and File Handling

A beginner-friendly console application to register students, collect course fees, search student records and display pending dues. All records are stored locally in `fees.txt`.

## Course fee structure

| Course | Total fee |
|---|---:|
| BCA | ₹45,000 |
| BTech | ₹80,000 |
| MBA | ₹80,000 |

## Features

- Add/register a student with roll number, name and course.
- Accept full or partial fee payments.
- Reject zero, negative and over-due payments.
- Search student details by roll number.
- List all students with pending dues.
- Calculate due amount and payment status automatically.
- Load records when the program starts and save after every change.
- Prevent duplicate roll numbers.

## Requirements

- Python 3.x
- No external packages are required.

## Run

Open a terminal in this project folder and execute:

```bash
python main.py
```

On Windows, this may also be:

```bash
py main.py
```

The application creates `fees.txt` automatically when the first student is added. Keep this file in the same folder as `main.py`; it contains the saved student records.

## Menu

1. Add Student
2. Pay Fee
3. Search by Roll Number
4. Pending Dues
5. Exit

## File format

Each line in `fees.txt` stores one record in this format:

```text
Roll|Name|Course|Paid
```

The total fee is taken from the course-fee dictionary, so it does not need to be duplicated in the file.

## Validation

- Roll number must be a positive whole number and must be unique.
- Student name cannot be empty.
- Course must be BCA, BTech or MBA.
- Payment must be a positive whole number.
- Payment cannot exceed the student's current due amount.

## Test scenarios from the college specification

| Test | Input / action | Expected result |
|---|---|---|
| 1. Normal input | Add roll 101, Riya, BCA | Total ₹45,000; Paid ₹0; Due ₹45,000; Unpaid |
| 2. Boundary input | Pay ₹45,000 for roll 101 | Paid ₹45,000; Due ₹0; Paid |
| 3. Invalid input | Try paying ₹50,000 when due is ₹45,000 | Payment rejected; record unchanged |
| 4. Different valid scenario | Add roll 102, Aman, BTech; pay ₹20,000 | Paid ₹20,000; Due ₹60,000; Partial; roll 102 appears in Pending Dues |

## Notes

- This is a console-based academic project, not a real payment gateway.
- `fees.txt` is generated at runtime and should not be deleted if saved records are needed.
