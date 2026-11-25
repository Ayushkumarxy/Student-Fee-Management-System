"""
Student Fee Management System
PS No. 64 | Python 3
A console-based application using dictionaries, functions, conditions and file handling.
"""

import os

DATA_FILE = "fees.txt"

# Course name : Total course fee
COURSE_FEES = {
    "BCA": 45000,
    "BTech": 80000,
    "MBA": 80000
}

# Each student is stored as a dictionary inside this list.
students = []


def calculate_due(student):
    """Return the remaining fee for a student."""
    return student["TotalFee"] - student["Paid"]


def get_status(student):
    """Return Unpaid, Partial or Paid according to the payment balance."""
    due = calculate_due(student)

    if student["Paid"] == 0:
        return "Unpaid"
    elif due == 0:
        return "Paid"
    return "Partial"


def save_records():
    """Save all student records to fees.txt."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            for student in students:
                # Comma-separated format follows the college specification.
                line = (
                    f'{student["Roll"]},{student["Name"]},'
                    f'{student["Course"]},{student["Paid"]}\n'
                )
                file.write(line)
    except OSError as error:
        print(f"Error: Could not save records. {error}")


def load_records():
    """Load student records from fees.txt when the program starts."""
    students.clear()

    if not os.path.exists(DATA_FILE):
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) != 4:
                    print(f"Warning: Invalid record on line {line_number}; skipped.")
                    continue

                roll, name, course, paid_text = parts

                try:
                    roll = int(roll)
                    paid = int(paid_text)
                except ValueError:
                    print(f"Warning: Invalid number on line {line_number}; skipped.")
                    continue

                course = course.strip()
                name = name.strip()

                if not name or course not in COURSE_FEES:
                    print(f"Warning: Invalid student data on line {line_number}; skipped.")
                    continue

                total_fee = COURSE_FEES[course]
                if roll <= 0 or paid < 0 or paid > total_fee:
                    print(f"Warning: Invalid fee data on line {line_number}; skipped.")
                    continue

                # Ignore duplicate roll numbers rather than loading duplicate students.
                if search_student(roll) is not None:
                    print(f"Warning: Duplicate roll number {roll}; later record skipped.")
                    continue

                students.append({
                    "Roll": roll,
                    "Name": name,
                    "Course": course,
                    "TotalFee": total_fee,
                    "Paid": paid
                })
    except OSError as error:
        print(f"Error: Could not read records. {error}")


def search_student(roll):
    """Find and return a student dictionary by roll number."""
    for student in students:
        if student["Roll"] == roll:
            return student
    return None


def add_student():
    """Register a student in a course."""
    print("\n--- Add Student ---")

    try:
        roll = int(input("Roll: ").strip())
    except ValueError:
        print("Invalid roll number. Please enter a whole number.")
        return

    if roll <= 0:
        print("Roll number must be greater than zero.")
        return

    if search_student(roll) is not None:
        print(f"Student with roll number {roll} already exists.")
        return

    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    print("Available courses:")
    for course, fee in COURSE_FEES.items():
        print(f"{course}: ₹{fee}")

    course = input("Course: ").strip()
    if course not in COURSE_FEES:
        print("Invalid course. Please select BCA, BTech or MBA.")
        return

    student = {
        "Roll": roll,
        "Name": name,
        "Course": course,
        "TotalFee": COURSE_FEES[course],
        "Paid": 0
    }

    students.append(student)
    save_records()

    print(
        f"Student added: {roll} | {name} | {course} | "
        f"Total Fee: {student['TotalFee']} | Paid: 0 | "
        f"Due: {calculate_due(student)} | Status: {get_status(student)}"
    )


def pay_fee():
    """Accept a valid fee payment for an existing student."""
    print("\n--- Pay Fee ---")

    try:
        roll = int(input("Roll: ").strip())
    except ValueError:
        print("Invalid roll number. Please enter a whole number.")
        return

    student = search_student(roll)
    if student is None:
        print(f"Student with roll number {roll} not found.")
        return

    due = calculate_due(student)
    if due == 0:
        print("No dues remaining. Student has already paid the total fee.")
        return

    try:
        amount = int(input("Amount: ").strip())
    except ValueError:
        print("Invalid amount. Please enter a whole number.")
        return

    if amount <= 0:
        print("Payment rejected. Amount must be greater than zero.")
        return

    if amount > due:
        print(f"Amount exceeds due ({due}). Payment rejected.")
        return

    student["Paid"] += amount
    save_records()

    print(
        f"Payment received. Paid: {student['Paid']} | "
        f"Due: {calculate_due(student)} | Status: {get_status(student)}"
    )


def search_by_roll():
    """Display one student's fee record using the roll number."""
    print("\n--- Search Student ---")

    try:
        roll = int(input("Roll: ").strip())
    except ValueError:
        print("Invalid roll number. Please enter a whole number.")
        return

    student = search_student(roll)
    if student is None:
        print("Student not found.")
        return

    print(
        f"Roll: {student['Roll']} | Name: {student['Name']} | "
        f"Course: {student['Course']} | Total Fee: {student['TotalFee']} | "
        f"Paid: {student['Paid']} | Due: {calculate_due(student)} | "
        f"Status: {get_status(student)}"
    )


def pending_dues():
    """List all students whose fee balance is greater than zero."""
    print("\n--- Pending Dues ---")

    pending_students = [
        student for student in students if calculate_due(student) > 0
    ]

    if not pending_students:
        print("No pending dues.")
        return

    print("Roll | Name | Course | Total Fee | Paid | Due | Status")
    print("-" * 72)

    for student in pending_students:
        print(
            f"{student['Roll']} | {student['Name']} | {student['Course']} | "
            f"{student['TotalFee']} | {student['Paid']} | "
            f"{calculate_due(student)} | {get_status(student)}"
        )


def display_menu():
    """Display the main menu."""
    print("\n========== STUDENT FEE MANAGEMENT SYSTEM ==========")
    print("1. Add Student")
    print("2. Pay Fee")
    print("3. Search by Roll Number")
    print("4. Pending Dues")
    print("5. Exit")
    print("====================================================")


def main():
    """Load saved data and run the console menu."""
    load_records()
    print("Student Fee Management System")
    print(f"Records loaded: {len(students)}")

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            pay_fee()
        elif choice == "3":
            search_by_roll()
        elif choice == "4":
            pending_dues()
        elif choice == "5":
            save_records()
            print("Thank you. Records saved. Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
