import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os


#-------------------------------------File containing student data-------------------------------------------------


script_dir = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(script_dir, "studentMarks.txt")

# --------------------------FUNCTIONS-------------------------------------------------------------------
#LOADS STUDENT DATA
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
            coursework_marks = list(map(int, parts[2:5]))                #Calculates the score, total percentage etc
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
                "grade": grade
            })
    return students

#Assigns grades
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

#----------------------------------------------------GUI Functions---------------------------------------------------

#Clears previous Treeview rows
def display_students(students):
    for row in tree.get_children():
        tree.delete(row)
    #Adds rows for each student
    for s in students:
        tree.insert("", "end", values=(
            s['name'],
            s['code'],
            s['coursework'],
            s['exam'],
            f"{s['percentage']:.2f}%",
            s['grade']
        ))
    #Calculates percentage
    if students:
        avg_percentage = sum(s['percentage'] for s in students) / len(students)
        summary_var.set(f"Number of students: {len(students)} | Average %: {avg_percentage:.2f}%")
    else:
        summary_var.set("No student records available.")

#View all students
def view_all():
    students = load_students()
    display_students(students)

#View individual student
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

#View highest total
def view_highest():
    students = load_students()
    if not students:
        return
    top_student = max(students, key=lambda s: s['total'])
    display_students([top_student])

#View lowest total
def view_lowest():
    students = load_students()
    if not students:
        return
    bottom_student = min(students, key=lambda s: s['total'])
    display_students([bottom_student])


#---------------------------------------------------Main GUI---------------------------------------------------------------

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

# Treeview style
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#FFD6E0", foreground="black", rowheight=25, fieldbackground="#FFD6E0")
style.map("Treeview", background=[("selected", "#FFB6C1")])  # Slightly darker pink for selection

# Treeview
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

