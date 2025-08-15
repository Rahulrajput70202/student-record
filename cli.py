# cli.py
"""
Menu-driven CLI for Student Performance Tracker.
Usage:
    python cli.py
"""
from tracker import StudentTracker

def main():
    tracker = StudentTracker()  # sqlite:///students.db by default

    def prompt_student():
        name = input("Enter student name: ").strip()
        roll = input("Enter roll number: ").strip()
        return name, roll

    while True:
        print("\n--- Student Performance Tracker (CLI) ---")
        print("1. Add Student")
        print("2. Add/Update Grades")
        print("3. View Student Details")
        print("4. Calculate Student Average")
        print("5. Subject-wise Topper (Bonus)")
        print("6. Class Average for Subject (Bonus)")
        print("7. Backup to Text File (Bonus)")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name, roll = prompt_student()
                s = tracker.add_student(name, roll)
                print(f"Added: {s.info()}")
            elif choice == "2":
                roll = input("Enter roll number: ").strip()
                grades = {}
                print("Enter subject=score (empty to stop). Example: Math=95")
                while True:
                    line = input("> ").strip()
                    if not line:
                        break
                    if "=" not in line:
                        print("Invalid format. Use subject=score")
                        continue
                    subj, score = line.split("=", 1)
                    grades[subj.strip()] = float(score.strip())
                s = tracker.add_grades(roll, grades)
                print(f"Updated: {s.info()}")
            elif choice == "3":
                roll = input("Roll number: ").strip()
                s = tracker.view_student_details(roll)
                print(s.info())
            elif choice == "4":
                roll = input("Roll number: ").strip()
                avg = tracker.calculate_average(roll)
                print(f"Average: {avg:.2f}")
            elif choice == "5":
                subject = input("Subject: ").strip()
                top = tracker.subject_topper(subject)
                if top:
                    name, roll, score = top
                    print(f"Topper in {subject}: {name} ({roll}) - {score}")
                else:
                    print("No data for that subject yet.")
            elif choice == "6":
                subject = input("Subject: ").strip()
                avg = tracker.class_average_for_subject(subject)
                if avg is None:
                    print("No data for that subject yet.")
                else:
                    print(f"Class average for {subject}: {avg:.2f}")
            elif choice == "7":
                path = tracker.export_to_txt()
                print(f"Exported to {path}")
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
