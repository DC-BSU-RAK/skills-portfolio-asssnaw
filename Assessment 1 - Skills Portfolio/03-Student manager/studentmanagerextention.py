import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os

#---------------------------File containing student data-----------------------------------------------------


script_dir = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(script_dir, "studentMarks.txt")


#-------------------------functions----------------------------------------------

def load_students():
    if not os.path.exists(FILE_PATH):
        messagebox.showerror("Error", f"File not found: {FILE_PATH}")
        return []

    students = []
    with open(FILE_PATH, "r") as f:
        lines = f.read().splitlines()
        if not lines:
            return []

        num_students = int(lines[0])
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) < 5:
                continue
            code = parts[0].strip()
            name = parts[1].strip()
            coursework_marks = list(map(int, parts[2:5]))
            exam_mark = int(parts[5])
            coursework_total = sum(coursework_marks)
            overall_total = coursework_total + exam_mark
            percentage = overall_total / 160 * 100
            grade = get_grade(percentage)
            students.append({
                "code": code,
                "name": name,
                "coursework": coursework_total,
                "exam": exam_mark,
                "total": overall_total,
                "percentage": percentage,
                "grade": grade,
                "raw_marks": coursework_marks  # store original marks for editing
            })
    return students

def save_students(students):
    with open(FILE_PATH, "w") as f:
        f.write(f"{len(students)}\n")
        for s in students:
            line = f"{s['code']},{s['name']},{s['raw_marks'][0]},{s['raw_marks'][1]},{s['raw_marks'][2]},{s['exam']}\n"
            f.write(line)

def get_grade(percentage):
    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


#---------------------------------------------GUI Functions------------------------------------------------------

def display_students(students):
    for row in tree.get_children():
        tree.delete(row)
    
    for s in students:
        tree.insert("", "end", values=(
            s['name'],
            s['code'],
            s['coursework'],
            s['exam'],
            f"{s['percentage']:.2f}%",
            s['grade']
        ))
    
    if students:
        avg_percentage = sum(s['percentage'] for s in students) / len(students)
        summary_var.set(f"Number of students: {len(students)} | Average %: {avg_percentage:.2f}%")
    else:
        summary_var.set("No student records available.")

#View all students
def view_all():
    students = load_students()
    display_students(students)

#View individual students
def view_individual():
    students = load_students()
    if not students:
        return
    query = simpledialog.askstring("Individual Student", "Enter student code or name:")
    if not query:
        return
    query = query.strip().lower()
    student = next((s for s in students if s['code'].lower() == query or s['name'].lower() == query), None)
    if student:
        display_students([student])
    else:
        messagebox.showinfo("Not Found", f"No student found matching '{query}'")

#view highest student
def view_highest():
    students = load_students()
    if not students:
        return
    top_student = max(students, key=lambda s: s['total'])
    display_students([top_student])

#view lowest student
def view_lowest():
    students = load_students()
    if not students:
        return
    bottom_student = min(students, key=lambda s: s['total'])
    display_students([bottom_student])

#----------------------------------------EXTENDED ACTIONS--------------------------------------------
#SORTS STUDENTS IN ASCENDING OR DESCENDING ORDER
def sort_students():
    students = load_students()
    if not students:
        return
    order = simpledialog.askstring("Sort Order", "Sort by Total (asc/desc):").strip().lower()
    if order not in ["asc", "desc"]:
        messagebox.showinfo("Invalid", "Enter 'asc' or 'desc'")
        return
    students.sort(key=lambda s: s['total'], reverse=(order=="desc"))
    display_students(students)

#Add students
def add_student():
    students = load_students()
    code = simpledialog.askstring("Add Student", "Enter student code:")
    if not code:
        return
    name = simpledialog.askstring("Add Student", "Enter student name:")
    if not name:
        return
    try:
        marks = []
        for i in range(1, 4):
            mark = simpledialog.askinteger("Add Student", f"Enter coursework mark {i} (0-20):", minvalue=0, maxvalue=20)
            marks.append(mark)
        exam = simpledialog.askinteger("Add Student", "Enter exam mark (0-100):", minvalue=0, maxvalue=100)
    except:
        messagebox.showerror("Invalid Input", "Marks must be numeric within allowed range")
        return
    coursework_total = sum(marks)
    overall_total = coursework_total + exam
    percentage = overall_total / 160 * 100
    grade = get_grade(percentage)
    students.append({
        "code": code.strip(),
        "name": name.strip(),
        "coursework": coursework_total,
        "exam": exam,
        "total": overall_total,
        "percentage": percentage,
        "grade": grade,
        "raw_marks": marks
    })
    save_students(students)
    display_students(students)

#Deletes students
def delete_student():
    students = load_students()
    if not students:
        return
    query = simpledialog.askstring("Delete Student", "Enter student code or name to delete:")
    if not query:
        return
    query = query.strip().lower()
    student = next((s for s in students if s['code'].lower() == query or s['name'].lower() == query), None)
    if student:
        students.remove(student)
        save_students(students)
        display_students(students)
        messagebox.showinfo("Deleted", f"Deleted student {student['name']}")
    else:
        messagebox.showinfo("Not Found", f"No student found matching '{query}'")

#Updates students
def update_student():
    students = load_students()
    if not students:
        return
    query = simpledialog.askstring("Update Student", "Enter student code or name to update:")
    if not query:
        return
    query = query.strip().lower()
    student = next((s for s in students if s['code'].lower() == query or s['name'].lower() == query), None)
    if not student:
        messagebox.showinfo("Not Found", f"No student found matching '{query}'")
        return
    
    # Submenu: choose what to update
    options = ["Name", "Code", "Coursework1", "Coursework2", "Coursework3", "Exam"]
    choice = simpledialog.askstring("Update Student", f"What to update? Options: {', '.join(options)}").strip()
    if choice not in options:
        messagebox.showinfo("Invalid", "Invalid choice")
        return
    
    try:
        if choice == "Name":
            new_value = simpledialog.askstring("Update Student", "Enter new name:")
            if new_value: student['name'] = new_value.strip()
        elif choice == "Code":
            new_value = simpledialog.askstring("Update Student", "Enter new code:")
            if new_value: student['code'] = new_value.strip()
        elif choice.startswith("Coursework"):
            idx = int(choice[-1])-1
            new_value = simpledialog.askinteger("Update Student", f"Enter new mark for {choice} (0-20):", minvalue=0, maxvalue=20)
            if new_value is not None:
                student['raw_marks'][idx] = new_value
        elif choice == "Exam":
            new_value = simpledialog.askinteger("Update Student", "Enter new exam mark (0-100):", minvalue=0, maxvalue=100)
            if new_value is not None: student['exam'] = new_value
    except:
        messagebox.showerror("Invalid Input", "Marks must be numeric within allowed range")
        return
    
    # Recalculate totals, percentage, grades etc
    student['coursework'] = sum(student['raw_marks'])
    student['total'] = student['coursework'] + student['exam']
    student['percentage'] = student['total']/160*100
    student['grade'] = get_grade(student['percentage'])
    
    save_students(students)
    display_students(students)
    messagebox.showinfo("Updated", f"Updated student {student['name']} successfully")


#---------------------------------------Main GUI----------------------------------------------------------------
root = tk.Tk()
root.title("Student Manager")
root.configure(bg="#FFC0CB")  # Baby pink background

# Menu
menubar = tk.Menu(root)
root.config(menu=menubar)

menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Options", menu=menu)
menu.add_command(label="View All Students", command=view_all)
menu.add_command(label="View Individual Student", command=view_individual)
menu.add_command(label="Student with Highest Total", command=view_highest)
menu.add_command(label="Student with Lowest Total", command=view_lowest)
menu.add_separator()
menu.add_command(label="Sort Students", command=sort_students)
menu.add_command(label="Add Student", command=add_student)
menu.add_command(label="Delete Student", command=delete_student)
menu.add_command(label="Update Student", command=update_student)

# Treeview style
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#FFD6E0", foreground="black", rowheight=25, fieldbackground="#FFD6E0")
style.map("Treeview", background=[("selected", "#FFB6C1")])  # Darker pink for selection


columns = ("Name", "Code", "Coursework", "Exam", "Percentage", "Grade")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill="both", expand=True, padx=10, pady=10)

# Summary label
summary_var = tk.StringVar()
summary_label = tk.Label(root, textvariable=summary_var, bg="#FFC0CB", font=("Arial", 12, "bold"))
summary_label.pack(pady=5)

# Load all students
view_all()

root.mainloop()

