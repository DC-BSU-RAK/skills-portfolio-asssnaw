import tkinter as tk                  #Imports the tkinter
from tkinter import messagebox        #Used for pop up messages
import random                         #For generating random numbers and +- operations


def displayMenu():                                                # Shows the first screen
    clear_window()                                                # Clears the screen before showing the menu
    root.configure(bg="#FFB6C1")                                # Baby pink background

    tk.Label(root, text="DIFFICULTY LEVEL",                       # Label to display the title
            font=("Arial", 20, "bold"),
            bg="#FFB6C1", fg="black").pack(pady=20)
    
#--------------------------------------------------THREE BUTTONS FOR DIFFERENT LEVELS--------------------------------------------------

# Easy Level
    tk.Button(root, text="1. Easy", width=20, bg="white", fg="black",  
            command=lambda: start_quiz('Easy')).pack(pady=8)      # Calls start_quiz() when "easy" level is selected

# Moderate Level
    tk.Button(root, text="2. Moderate", width=20, bg="white", fg="black",
            command=lambda: start_quiz('Moderate')).pack(pady=8)  # Calls start_quiz() when "Moderate" level is selected

# Advanced Level
    tk.Button(root, text="3. Advanced", width=20, bg="white", fg="black",
            command=lambda: start_quiz('Advanced')).pack(pady=8)  # Calls start_quiz() when "Advanced" level is selected

#".pack" arranges the buttons vertically



#------------------------------------------------------RANDOM NUMBERS----------------------------------------------------
def randomInt(level):                                      # Chooses numerical based on difficulty level chosen
    if level == 'Easy':                                    # Easy level chooses single digit numbers, i.e 1-9
        return random.randint(1, 9)                        # "random.randint(1, 9)" returns a random integer between 1 and 9.


    elif level == 'Moderate':                              # Moderate level chooses double digit number, i.e 10-99
        return random.randint(10, 99)                      # "random.randint(10, 99)" returns a random integer between 10 and 99.


    elif level == 'Advanced':                              # Advanced level chooses 4-digit number, i.e 1000-9999
        return random.randint(1000, 9999)                  # "random.randint(1000, 9999)" returns a random integer between 1000 and 9999.


#------------------------------------------------------RANDOM OPERATIONS-------------------------------------------------
def decideOperation():                                    # Decides randomly if the operation is + or - for each question
    return random.choice(['+', '-'])                      # "random.choice(['+','-'])" picks one from the element either + or -


#----------------------------------------------------NEXT QUESTION-------------------------------------------------------
def displayProblem():                                     # Creates and displays next question
    global num1, num2, operation, attempt, question_count, answer_entry

    if question_count >= 10:                              # Stops after 10 questions
        displayResults()
        return

    clear_window()
    root.configure(bg="#FFB6C1")

    num1 = randomInt(difficulty)                         # Generates random numbers and operations
    num2 = randomInt(difficulty)
    operation = decideOperation()
    attempt = 1                                         # Keeps a track of attempts made by the user

    tk.Label(root, text=f"Question {question_count + 1}/10",  # Displays the question number
            font=("Arial", 14, "bold"), bg="#FFB6C1", fg="black").pack(pady=10)

    tk.Label(root, text=f"{num1} {operation} {num2} =",      # Displays the question
            font=("Arial", 24), bg="#FFB6C1", fg="black").pack(pady=10)

    answer_entry = tk.Entry(root, font=("Arial", 16), justify="center")   #For users to type the answer
    answer_entry.pack(pady=5)
    answer_entry.focus()                                                  # Automatically drags the cruiser here

    tk.Button(root, text="Submit", bg="white", fg="black",               # Button tu submit the answer
            command=checkAnswer).pack(pady=10)


#------------------------------------------------COMPARES THE ANSWERS---------------------------------------------------
def isCorrect(user_answer):                           # Checks if the user's answer is correct
    if operation == '+':
        correct_answer = num1 + num2
    else:
        correct_answer = num1 - num2
    return user_answer == correct_answer             # Returns true if correct, False if not



#---------------------------------------------SCORES----------------------------------------------------------------------
def checkAnswer():                                      # Handles answer checking and scoring points
    global score, question_count, attempt

    try:
        user_answer = int(answer_entry.get())           # Reads the input and validates if its an integer
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid number!")
        return

    if isCorrect(user_answer):                           # If correct on first try user scores 10 points 
        if attempt == 1:
            score += 10
            messagebox.showinfo("Correct!", "🎉 Well done! +10 points")
        else:
            score += 5                                   # If correct on second try user scores 5 points
            messagebox.showinfo("Correct!", "😊 Good! +5 points")
        question_count += 1
        displayProblem()
    else:
        if attempt == 1:
            attempt += 1
            messagebox.showinfo("Try Again", "❌ Incorrect! Try once more.") # If incorrect the first try user gets a second chance 
        else:
            messagebox.showinfo("Wrong", "Incorrect again! Moving to next question.") # If wrong both times moves on to the next question
            question_count += 1
            displayProblem()


#------------------------------------------------------------FINAL SCORES----------------------------------------------------
def displayResults():                                    # Displays the final score and grades
    clear_window()
    root.configure(bg="#FFB6C1")

# CALCULATION OF THE GRADE
    if score >= 90:
        grade = "A+"                                     # Above or 90 is A+
    elif score >= 75:
        grade = "A"                                      # Above or 75 is A
    elif score >= 60:
        grade = "B"                                      # Above or 60 is B
    elif score >= 45:
        grade = "C"                                      # Above or 45 is C
    else:
        grade = "F"                                      # Below 45 is F

# THE FINAL MESSAGES
    tk.Label(root, text="🎯 QUIZ COMPLETED 🎯",                                     # Displays the text quiz completed
            font=("Arial", 20, "bold"), bg="#FFB6C1", fg="black").pack(pady=10)
    tk.Label(root, text=f"Your final score: {score}/100",                            # Displays the final score out of 100
            font=("Arial", 16), bg="#FFB6C1", fg="black").pack(pady=5)
    tk.Label(root, text=f"Grade: {grade}",                                           # Displays the grade A+, A, B, C, F
            font=("Arial", 16, "bold"), bg="#FFB6C1", fg="black").pack(pady=5)

# BUTTONS TO REPLAY OR EXIT THE QUIZ
    tk.Button(root, text="Play Again", bg="white", fg="black",                       # Button to Pay the quiz again
            command=displayMenu).pack(pady=10)
    tk.Button(root, text="Exit", bg="white", fg="black",                             # Button to Exit the quiz
            command=root.destroy).pack(pady=5)


#---------------------------------------------------STARTS THE QUIZ----------------------------------------------------------
def start_quiz(level):                                          # Begins the Quiz
    global difficulty, score, question_count
    difficulty = level                                          # Stores selected difficulty level
    score = 0                                                   # Resets the score to 0
    question_count = 0                                          # Resets the question counter
    displayProblem()                                            # Starts displaying questions


def clear_window():                                             # Clears the window white switching the screens
    for widget in root.winfo_children():
        widget.destroy()


#---------------------------------------------------MAIN PROGRAM------------------------------------------------------------
root = tk.Tk()                                       # Creates main application window
root.title("Math Quiz 💖")                # Title display on the window bar
root.geometry("400x420")                             # Sets window size
root.resizable(False, False)                         # Sets the fixed window size
root.configure(bg="#FFB6C1")                      # Sets the background color to baby pink

score = 0                                          # initializes the global score
question_count = 0                                 # initializes the question count

displayMenu()                                     # Starts by showing main menu, i.e difficulty menu

root.mainloop()
