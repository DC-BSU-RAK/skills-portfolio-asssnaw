import tkinter as tk
from tkinter import messagebox              #to show pop ups
import random                               #to generate random numbers
import time                                 # for the timer

#--------------------------------------------------SETTING TIMER--------------------------------------------------------------
TIME_PER_QUESTION = 20  # sets timer 20 seconds per question

# --------------------------------------------------STORING DATA---------------------------------------------------------------
custom_questions = []   # Stores user created questions (list of tuples)
question_stats = []     # Stores performance data per question

# ---------------------------------------------------UTILITY FUNCTIONS---------------------------------------------------------
def clear_window():
    try:
        root.unbind('<Return>')                     # Unbind Enter key to avoid duplicate triggers when screens changes
    except Exception:
        pass

    for widget in root.winfo_children():            #Removes all widgets from window to show a new screen
        widget.destroy()

#---------This function safely evaluates addition or subtraction and ignores any invalid character
def evaluate_expression(expr):
    try:
        safe = "".join(c for c in expr if c.isdigit() or c in "+- ")
        return int(eval(safe))
    except Exception:
        return None         # Returns NONE if operation can not be evaluated 

# ---------------------------------------------------- WELCOME PAGE ------------------------------------------------------------
def welcomePage():
    clear_window()      #Clears the window
    root.configure(bg="#FFB6C1")  #Sets Pink background

    tk.Label(root, text="WELCOME TO THE QUIZ 🎉",                #Displays the Title
            font=("Arial", 36, "bold"),
            bg="#FFB6C1", fg="black").pack(pady=100)

    tk.Button(root, text="LET'S GET STARTED", bg="white", fg="black",         #Displays the start button of the quiz
            font=("Arial", 24, "bold"), width=20,
            command=userName).pack(pady=50)                         #The start button leads to next page where user is asked for name

# ----------------------------------------------------USERS NAME PAGE------------------------------------------------------------
def userName():
    clear_window()
    root.configure(bg="#FFB6C1")

    tk.Label(root, text="ENTER YOUR NAME 💖",               #Displays text asking user to type their name
            font=("Arial", 28, "bold"),
            bg="#FFB6C1", fg="black").pack(pady=30)

    global name_entry                                      
    name_entry = tk.Entry(root, font=("Arial", 20), justify="center") #Creates a text input box for user to type their name
    name_entry.pack(pady=10)   #Adds vertical spacing around the entry box
    name_entry.focus()  # automatically sets cursor inside the box 

    tk.Button(root, text="Continue", bg="white", fg="black",    #Lets the user to submit their name and continue onto the next page
            font=("Arial", 14), command=saveName).pack(pady=20)

#Saves the name and shows warning if left empty
def saveName():
    global user_name
    user_name = name_entry.get().strip()
    if user_name == "":
        messagebox.showwarning("Name Missing", "Please enter your name!")
        return
    displayMenu()  #proceeds to the main page

# --------------------------- -------------------------MAIN PAGE--------------------------------------------------------------
def displayMenu():
    clear_window()
    root.configure(bg="#FFB6C1")

    tk.Label(root, text=f"Welcome {user_name}! 💗",                        #Displays text welcoming the user
            font=("Arial", 24, "bold"),
            bg="#FFB6C1", fg="black").pack(pady=20)

    tk.Label(root, text="SELECT MODE",                                     #Displays a text asking the user to select a mode
            font=("Arial", 20, "bold"),
            bg="#FFB6C1", fg="black").pack(pady=10)

    tk.Button(root, text="Play a Challenging Quiz", width=20, bg="white",  #An option for user to play a quiz 
            font=("Arial", 14), command=difficultyLevel).pack(pady=8)      #When selected leads to the difficulty level page

    tk.Button(root, text="Create Your Own Quiz", width=20, bg="white",     #An option for user to create their own quiz
            font=("Arial", 14), command=createQuiz).pack(pady=8)           #When selected leads to the create quiz page

    tk.Button(root, text="Exit", width=20, bg="white",                     #An option for users to exit the quiz
            font=("Arial", 14), command=root.destroy).pack(pady=16)        #Destroys the page when selected 

# ---------------------------------------------DIFFICULTY LEVEL SELECTION---------------------------------------------------------
def difficultyLevel():
    clear_window()
    root.configure(bg="#FFB6C1")

    tk.Label(root, text="DIFFICULTY LEVEL",                   #Displays the text
            font=("Arial", 24, "bold"),
            bg="#FFB6C1", fg="black").pack(pady=20)

    tk.Button(root, text="Easy", width=20, bg="white",                                  #Easy level 
            font=("Arial", 14), command=lambda: start_quiz('Easy')).pack(pady=8)

    tk.Button(root, text="Moderate", width=20, bg="white",                              #Moderate level
            font=("Arial", 14), command=lambda: start_quiz('Moderate')).pack(pady=8)

    tk.Button(root, text="Advanced", width=20, bg="white",                              #Advanced level
            font=("Arial", 14), command=lambda: start_quiz('Advanced')).pack(pady=8)

# -----------------------------------------CUSTOM QUIZ CREATION------------------------------------------------------------------
def createQuiz():
    clear_window()
    root.configure(bg="#FFB6C1")

    tk.Label(root, text="Create Math Quiz 📝",                 #Displays text
            font=("Arial", 24, "bold"),
            bg="#FFB6C1", fg="black").pack(pady=18)

    tk.Label(root, text="Enter number of questions:",             #Asks the user to enter the number of question they want to create
            font=("Arial", 16), bg="#FFB6C1").pack(pady=(8,0))

    global num_q_entry                                            
    num_q_entry = tk.Entry(root, font=("Arial", 16), justify="center")      #Entry box for the user to type
    num_q_entry.pack(pady=8)

    tk.Button(root, text="Start", bg="white", font=("Arial", 14),   #This button leads to a page where user starts creating questions
            command=startCreatingQuestions).pack(pady=12)

#--------------------------------------CREATING QUESTIONS-----------------------------------------------------------------------
def startCreatingQuestions():
    global custom_total, custom_count   #Keeps track of number of questions the user wants to create
    try:
        custom_total = int(num_q_entry.get())  #Entry box for user to type in the text
        if custom_total <= 0:
            raise ValueError       #If the number is 0 or negative it raises a ValueError
    except Exception:
        messagebox.showerror("Invalid", "Enter a valid positive number!")
        return

    custom_questions.clear()   #Makes sure each quiz starts with an empty list
    custom_count = 0  #Resets custom counts
    askCustomQuestion() 

def askCustomQuestion():
    clear_window()
    root.configure(bg="#FFB6C1")

    tk.Label(root, text=f"Question {custom_count + 1}/{custom_total}",     #Shows number of questions made and number of questions to be made
            font=("Arial", 18, "bold"), bg="#FFB6C1").pack(pady=12)

    tk.Label(root, text="Enter math expression (e.g., 15 + 6):",   #Asks user to type expression along with example
            font=("Arial", 14), bg="#FFB6C1").pack(pady=(6,0))

    global custom_question_entry       #Creates a entry box where user can type math expression
    custom_question_entry = tk.Entry(root, font=("Arial", 16), justify="center", width=30)
    custom_question_entry.pack(pady=6)

    tk.Label(root, text="Enter correct answer (number):",         #Asks the user to type correct answer to the question
            font=("Arial", 14), bg="#FFB6C1").pack(pady=(8,0))

    global custom_answer_entry               #entry box where the user types correct answer
    custom_answer_entry = tk.Entry(root, font=("Arial", 16), justify="center", width=20)
    custom_answer_entry.pack(pady=6)

    tk.Button(root, text="Save", bg="white", font=("Arial", 14),  #Stores the data and moves on to next question
            command=saveCustomQuestion).pack(pady=12)

#saves the question and moves on to the next question or starts custom quiz-----------------------------------------------
def saveCustomQuestion():
    global custom_count
    question = custom_question_entry.get().strip()
    ans_text = custom_answer_entry.get().strip()

    if question == "" or ans_text == "":
        messagebox.showwarning("Missing", "Fill both fields!")
        return

    try:
        ans = int(ans_text)
    except Exception:
        messagebox.showwarning("Invalid", "Answer must be an integer number!")
        return

    custom_questions.append((question, ans))
    custom_count += 1

    if custom_count >= custom_total:
        start_custom_quiz()
    else:
        askCustomQuestion()

# --------------------------- RANDOM NUMBER & OPERATION FOR NORMAL QUIZ --------------------------------------------------
def randomInt(level):
    if level == 'Easy':                               #Easy level chooses random numbers between 1-9
        return random.randint(1, 9)
    elif level == 'Moderate':                         #Moderate level chooses random number between 10-99
        return random.randint(10, 99)
    else:                                             #Advanced level chooses random numbers between 100-9999
        return random.randint(100, 9999)

def decideOperation():
    return random.choice(['+', '-'])                  #Randomly chooses between + or -

# ------------------------------------------------START QUIZ----------------------------------------------------------------
def start_quiz(level):
    global difficulty, score, question_count, using_custom_quiz    #RESETS VARIABLES AND STARTS WITH FIRST QUESTION
    using_custom_quiz = False
    difficulty = level
    score = 0
    question_count = 0
    question_stats.clear()
    displayProblem()

def start_custom_quiz():
    global custom_index, score, using_custom_quiz
    using_custom_quiz = True
    score = 0
    custom_index = 0
    question_stats.clear()
    displayProblem()

# --------------------------------------------------QUESTION DISPLAY WITH TIMER----------------------------------------------
def displayProblem():
    global num1, num2, operation, attempt, timer_val, answer_entry
    global timer_job, start_time, question_index_global

    clear_window()
    root.configure(bg="#FFB6C1")

    attempt = 1
    timer_val = TIME_PER_QUESTION        #timer resets to full value

#CUSTOM QUIZ
    if using_custom_quiz:
        if custom_index >= len(custom_questions):          #if all questions done displays the final result
            displayResults()
            return
        question_text = custom_questions[custom_index][0] #gets questions from the list
        question_index_global = custom_index              #Saves the question displayed
        display_label = f"Question {custom_index + 1}/{len(custom_questions)}" #shows number of questions attended and total number of questions
        q_display = question_text #math equation displayed on screen
#NORMAL QUIZ
    else:
        if question_count >= 10:  #Displays result after 10 questions
            displayResults()
            return
        num1 = randomInt(difficulty) #Generate first number based on difficulty
        num2 = randomInt(difficulty) #Generates second number based on difficulty
        operation = decideOperation() #Picks random equation
        display_label = f"Question {question_count + 1}/10" #shows number of questions attended and total number of questions
        q_display = f"{num1} {operation} {num2}" #Prepares display question in string value

    tk.Label(root, text=display_label, #Creates label that shows progress
            font=("Arial", 20, "bold"), bg="#FFB6C1").pack(pady=(20,8))

    tk.Label(root, text=q_display, #displays the math question
            font=("Arial", 36), bg="#FFB6C1").pack(pady=(6,18))

    answer_entry = tk.Entry(root, font=("Arial", 22), justify="center", width=8) #creates text input for user
    answer_entry.pack(pady=6)
    answer_entry.focus()

    root.bind('<Return>', lambda event: checkAnswer()) #Binds the enter button to submit

    tk.Button(root, text="Submit", bg="white", font=("Arial", 14),
            command=checkAnswer).pack(pady=12)                      #Creates a Submit Button

    global timer_label
    timer_label = tk.Label(root, text=f"⏳ Time Left: {timer_val}s",   #Displays remaining time left
                        font=("Arial", 18, "bold"), bg="#FFB6C1")
    timer_label.pack(pady=8)

    start_time = time.time() #Useful to record how long the user took to answer
    try:
        if timer_job is not None:           #Prevents multiple timer loops running at the same time
            root.after_cancel(timer_job)
    except NameError:
        pass

    updateTimer() #Starts the countdown

def updateTimer():
    global timer_val, timer_job, start_time
    timer_label.config(text=f"⏳ Time Left: {timer_val}s") #updates timer text 
    timer_val -= 1 #reduces time by 1 second

#if the countdown ends a pop up alerts the user that time is up and the next question starts
    if timer_val < 0:
        messagebox.showinfo("Time’s Up!", "⏰ Time's up for this question! Moving to next.")
        record_performance_on_timeout()
        wrongAndNext(time_out=True)
        return

#This creates loop for timer which ends at 0 or stops when the user answers
    timer_job = root.after(1000, updateTimer)

# -------------------------------------------PERFORMANCE DATA STORAGE-----------------------------------------------------------

#Compares users answer with correct answer
def compute_correct_answer_generated():
    if operation == '+':
        return num1 + num2
    else:
        return num1 - num2

#Saves performance data into a list which is analyzed in the end of the quiz
def record_stat(question_text, time_taken, points, correct, attempts, idx):
    question_stats.append({
        'question': question_text,         #Question displayed
        'time': round(time_taken, 2),      #Time taken to answer
        'points': points,                  #Points awarded per question
        'correct': correct,                #If the answer is correct or not
        'attempts': attempts,              #Number of attempts by user
        'index': idx                       #Question number in the quiz
    })

#If user fails to attempt the question the response is still recorded
def record_performance_on_timeout():
    if using_custom_quiz:
        q_text = custom_questions[custom_index][0]
        idx = custom_index
    else:
        q_text = f"{num1} {operation} {num2}"
        idx = question_count

    record_stat(q_text, TIME_PER_QUESTION, 0, False, 0, idx)

# ---------------------------------------------CHECKING ANSWER---------------------------------------------------------------
#Checks if user answer is correct
def isCorrect(user_answer):
    if using_custom_quiz:  #Compares to the answer stored if custom quiz
        return user_answer == custom_questions[custom_index][1]
    else:
        return user_answer == compute_correct_answer_generated() #Compares with automatically generated mathematical answer in normal quiz

def checkAnswer():
    global score, question_count, attempt, custom_index, timer_job

    try:
        user_answer = int(answer_entry.get().strip()) #Reads the value from input box and converts into integer
    except Exception:
        messagebox.showwarning("Invalid Input", "Please enter a valid number!") #if input is not a valid number it shows warning
        return

    try:                                      #Stops the countdown after the user submits the answer
        if timer_job is not None:
            root.after_cancel(timer_job)
    except NameError:
        pass

    elapsed = max(0, time.time() - start_time) #Calculates the time taken by user to answer

    if isCorrect(user_answer):   #Checks if user's answer matches the correct answer
        points = 10 if attempt == 1 else 5   #first try=10pts second try=5pts 
        if attempt == 1:
            messagebox.showinfo("Correct!", f"🎉 Well done! +{points} points")
        else:
            messagebox.showinfo("Correct!", f"😊 Good! +{points} points (2nd attempt)")

#If played in custom mode
        if using_custom_quiz:
            q_text = custom_questions[custom_index][0]  #Gets the question text from the custom question list
            idx = custom_index                          #Stores its index
            custom_index += 1                           #Moves to the next custom question
#If played in normal mode
        else:
            q_text = f"{num1} {operation} {num2}"       #Generates a question
            idx = question_count                        #Stores its index
            question_count += 1                         #Moves on to the next generated question

        record_stat(q_text, elapsed, points, True, attempt, idx) #Saves performance data
        score += points                                          #Adds earned points to total
        displayProblem()                                         #Loads next question
    else:
        if attempt == 1:                                                       #IF first attempt is wrong
            attempt += 1                                                       #Increases the number of attempts
            messagebox.showinfo("Try Again", "❌ Incorrect! Try once more.")   #Asks user to try again
            updateTimer()                                                      #Resumes the timer
        else:
            messagebox.showinfo("Wrong", "Incorrect again! Moving to next question.") #if wrong at second attempt moves onto the next question along with a pop up
            if using_custom_quiz: #moves to the next custom question
                q_text = custom_questions[custom_index][0]
                idx = custom_index
                custom_index += 1
            else:
                q_text = f"{num1} {operation} {num2}" #Moves on to the next generated question
                idx = question_count
                question_count += 1

            record_stat(q_text, elapsed, 0, False, 2, idx)
            displayProblem()

#used when time runs out
def wrongAndNext(time_out=False):
    global question_count, custom_index
    if time_out:
        if using_custom_quiz:
            custom_index += 1
        else:
            question_count += 1
        try:
            if timer_job is not None:
                root.after_cancel(timer_job)
        except NameError:
            pass
        displayProblem()
        return

    try:
        if timer_job is not None:
            root.after_cancel(timer_job)
    except NameError:
        pass
    displayProblem()

# ---------------------------------------------------FINAL SCORE--------------------------------------------------------------
#Clears window and stops timer
def displayResults():
    clear_window()
    root.configure(bg="#FFB6C1")
    try:
        if timer_job is not None:
            root.after_cancel(timer_job)
    except NameError:
        pass
#Calculates grade based on score
    grade = ("A+" if score >= 90 else
            "A" if score >= 75 else
            "B" if score >= 60 else
            "C" if score >= 45 else "F")

#THE FINAL SCORE DISPLAY
    tk.Label(root, text="🎯 QUIZ COMPLETED 🎯",
            font=("Arial", 32, "bold"), bg="#FFB6C1").pack(pady=(20,10))

    tk.Label(root, text=f"Player: {user_name}",
            font=("Arial", 20), bg="#FFB6C1").pack(pady=(4,4))

    tk.Label(root, text=f"Final Score: {score}",
            font=("Arial", 20), bg="#FFB6C1").pack(pady=(2,2))

    tk.Label(root, text=f"Grade: {grade}",
            font=("Arial", 20, "bold"), bg="#FFB6C1").pack(pady=(6,10))

    sorted_qs = sorted(question_stats, key=lambda x: (x['time'], -x['points']))
    top3 = sorted_qs[:3]

    tk.Label(root, text="Top 3 Question Performances (Fastest → Slower)",
            font=("Arial", 18, "bold"), bg="#FFB6C1").pack(pady=(12,8))

    if not question_stats:
        tk.Label(root, text="No question data to show.", font=("Arial", 14), bg="#FFB6C1").pack(pady=8)
    else:
        rank_emojis = ["🥇 1st", "🥈 2nd", "🥉 3rd"]
        for i in range(3):
            if i < len(top3):
                s = top3[i]
                q_text = s['question']
                text = f"{rank_emojis[i]} — Q: {q_text} — Time: {s['time']}s — Points: {s['points']} — Attempts: {s['attempts']}"
            else:
                text = f"{rank_emojis[i]} — N/A"
            tk.Label(root, text=text, font=("Arial", 14), bg="#FFB6C1").pack(pady=4)

#PLAY AGAIN BUTTON
    tk.Button(root, text="Play Again", bg="white", font=("Arial", 14),
            command=welcomePage).pack(pady=(12,6))
#EXIT BUTTON
    tk.Button(root, text="Exit", bg="white", font=("Arial", 14),
            command=root.destroy).pack(pady=6)

# ---------------------------------------------------MAIN WINDOW SETUP----------------------------------------------------------
root = tk.Tk()
root.title("Math Quiz 💖")

# Starting size with minimize/maximize allowed
root.geometry("1024x768")
root.resizable(True, True)
root.configure(bg="#FFB6C1")

# Initialize globals
user_name = ""
score = 0
question_count = 0
using_custom_quiz = False

# Start flow with welcome page
welcomePage()

# Enter main loop
root.mainloop()
