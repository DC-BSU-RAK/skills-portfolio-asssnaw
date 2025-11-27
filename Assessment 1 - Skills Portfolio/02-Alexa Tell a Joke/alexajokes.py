import tkinter as tk                  #Creates app
from tkinter import messagebox        #Shows pop up message
import random                         #Used to pick random jokes
import os                             #helps locate file

# -----------------------------------------------------LOAD JOKES--------------------------------------------------------------

#Reads every line of the joke file and splits the statement into 2 parts question and punchline which is saved in the file format
def load_jokes():
    jokes = []
    file_path = os.path.join(os.path.dirname(__file__), "randomJokes.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup + "?", punchline))
    except FileNotFoundError:
        messagebox.showerror("File Not Found", f"{file_path} not found.") #if file missing error pops up
    return jokes

jokes_list = load_jokes() #jokes loaded from file
current_joke = None #jokes currently being shown
score = 0 #total points during game
username = ""  # User's name

# ----------------------------------------------------PAGE FUNCTIONS-----------------------------------------------------------
def show_welcome_page():
    clear_window()
    global username

    heading = tk.Label(root, text="HEAR A JOKE FROM ALEXA",           #Displays heading
                    font=("Arial", 24, "bold"), bg="#CD9EC4")
    heading.pack(pady=40)

    name_label = tk.Label(root, text="Enter your name:", font=("Arial", 16), bg="#CD9EC4") #Displays text asking user to type their name
    name_label.pack(pady=10)

    name_entry = tk.Entry(root, font=("Arial", 16)) #Entry box for user to type their name
    name_entry.pack(pady=10)

    def start():
        global username
        entered_name = name_entry.get().strip()
        if entered_name == "":
            messagebox.showwarning("Input Required", "Please enter your name to continue!") #If name not typed warning pops up
            return
        username = entered_name
        show_option_page()

    start_btn = tk.Button(root, text="Let's Get Started",               #Lets get started button
                        font=("Arial", 16), width=20, command=start)
    start_btn.pack(pady=20)

def show_option_page():
    clear_window()
    heading = tk.Label(root, text=f"Welcome, {username}!\nChoose an Option",  #Displays text
                    font=("Arial", 22, "bold"), bg="#CD9EC4")
    heading.pack(pady=50)

    tell_joke_btn = tk.Button(root, text="TELL ME A JOKE",                         #Button asking alexa to tell a joke
                            font=("Arial", 16), width=20, command=show_joke_page)
    tell_joke_btn.pack(pady=20)

    play_game_btn = tk.Button(root, text="PLAY A GAME",                            #Button asking users to play a game
                            font=("Arial", 16), width=20, command=show_game_page)
    play_game_btn.pack(pady=20)

# ---------------------------------------------------------JOKE PAGE-----------------------------------------------------------
def show_joke_page():                   #removes any existing widgets
    clear_window()
    global current_joke

    joke_label = tk.Label(root, text="LETS HEAR A JOKE!",
                        font=("Arial", 18), wraplength=550, bg="#CD9EC4")
    joke_label.pack(pady=(50, 10))

    punchline_label = tk.Label(root, text="",    
                            font=("Arial", 16, "italic"), wraplength=550, bg="#CD9EC4")
    punchline_label.pack(pady=(10, 30))

    btn_frame = tk.Frame(root, bg="#CD9EC4")
    btn_frame.pack(pady=20)

    def tell_joke():
        global current_joke
        if not jokes_list:
            joke_label.config(text="No jokes available!")
            punchline_label.config(text="")
            return
        current_joke = random.choice(jokes_list)
        joke_label.config(text=current_joke[0])
        punchline_label.config(text="")

    def show_punchline():
        if current_joke:
            punchline_label.config(text=current_joke[1])

    def next_joke():
        tell_joke()

    def back_to_options():
        show_option_page()

    tk.Button(btn_frame, text="Alexa tell me a Joke", font=("Arial", 14), width=20, command=tell_joke).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Show Punchline", font=("Arial", 14), width=20, command=show_punchline).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(btn_frame, text="Next Joke", font=("Arial", 14), width=20, command=next_joke).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Back", font=("Arial", 14), width=20, command=back_to_options).grid(row=1, column=1, padx=5, pady=5)

# -------------------------------------------------GAME PAGE--------------------------------------------------------------------
def show_game_page():
    clear_window()                  #Clears previous screen
    global current_joke, score

    score = 0
    question_count = 0
    MAX_QUESTIONS = 5     #total rounds

    score_label = tk.Label(root, text=f"{username}'s Score: {score}", font=("Arial", 16, "bold"), bg="#CD9EC4")
    score_label.pack(pady=20)  #Players current score

    joke_label = tk.Label(root, text="", font=("Arial", 18), wraplength=550, bg="#CD9EC4")
    joke_label.pack(pady=(30, 10))  #Joke setup

    entry = tk.Entry(root, font=("Arial", 16), width=40)
    entry.pack(pady=10)   #Entry box

    feedback_label = tk.Label(root, text="", font=("Arial", 14), bg="#CD9EC4")
    feedback_label.pack(pady=10) #Shows if answer is correct or wrong

    def new_joke():
        nonlocal question_count
        global current_joke
        if question_count >= MAX_QUESTIONS:
            messagebox.showinfo("Game Over", f"Game over! {username}'s final score: {score}")
            show_option_page()
            return
        if not jokes_list:
            joke_label.config(text="No jokes available!")
            return
        current_joke = random.choice(jokes_list)
        joke_label.config(text=current_joke[0])
        entry.delete(0, tk.END)
        feedback_label.config(text="")
        question_count += 1

#Compares the joke with actual answer, updates score and moves on to the next joke
    def check_answer():
        global score
        user_answer = entry.get().strip().lower()
        if current_joke:
            correct_answer = current_joke[1].strip().lower()
            if user_answer == correct_answer:
                score += 10
                feedback_label.config(text="Correct! +10 points")
            else:
                feedback_label.config(text=f"Wrong! Correct answer: {current_joke[1]}")
            score_label.config(text=f"{username}'s Score: {score}")
            new_joke()

#Provides hint
    def show_thumbnail():
        if current_joke:
            thumbnail = " ".join(current_joke[1].split()[:3]) + "..."
            feedback_label.config(text=f"Hint: {thumbnail}")

#Returns to main menu
    def back_to_options():
        show_option_page()

    tk.Button(root, text="Submit Answer", font=("Arial", 14), width=20, command=check_answer).pack(pady=5) #Checks answer
    tk.Button(root, text="Next Joke", font=("Arial", 14), width=20, command=new_joke).pack(pady=5) #Next new joke
    tk.Button(root, text="Give Hint", font=("Arial", 14), width=20, command=show_thumbnail).pack(pady=5) #shows first three words of the punchline
    tk.Button(root, text="Back", font=("Arial", 14), width=20, command=back_to_options).pack(pady=5) # back to main menu

    new_joke() #Starts the game

# clears window moving onto a new page
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# --------------------------------------------------MAIN TKINTER WINDOW-----------------------------------------------
root = tk.Tk()
root.title("Alexa TELLS A JOKE")
root.geometry("600x500")
root.configure(bg="#CD9EC4")

show_welcome_page()
root.mainloop()

