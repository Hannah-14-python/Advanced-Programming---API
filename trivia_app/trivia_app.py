import tkinter as tk
import requests
import random

class TriviaGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Trivia Quiz Game")
        self.master.geometry("600x400")  
        self.master.configure(bg="#f0f0f0")  

        self.score = 0
        self.question_number = 0
        self.questions = []
        self.timer = None
        self.time_left = 30  

        self.create_widgets()

    def create_widgets(self):

        self.title_label = tk.Label(self.master, text="Welcome to the Trivia Quiz!", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=10)


        self.category_label = tk.Label(self.master, text="Select Category:", font=("Helvetica", 12), bg="#f0f0f0")
        self.category_label.pack(pady=5)

        self.category_var = tk.StringVar(value="General Knowledge")
        self.category_menu = tk.OptionMenu(self.master, self.category_var,
                                            "General Knowledge",  
                                            "Science: Computers",  
                                            "Entertainment: Books", 
                                            "Entertainment: Film",  
                                            "Entertainment: Music")  
        self.category_menu.config(font=("Helvetica", 12), bg="#ffffff")
        self.category_menu.pack(pady=5)

        self.difficulty_label = tk.Label(self.master, text="Select Difficulty:", font=("Helvetica", 12), bg="#f0f0f0")
        self.difficulty_label.pack(pady=5)

        self.difficulty_var = tk.StringVar(value="Easy")
        self.difficulty_menu = tk.OptionMenu(self.master, self.difficulty_var, "Easy", "Medium", "Hard")
        self.difficulty_menu.config(font=("Helvetica", 12), bg="#ffffff")
        self.difficulty_menu.pack(pady=5)

        self.start_button = tk.Button(self.master, text="Start Quiz", command=self.start_quiz, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.start_button.pack(pady=20)

        self.question_label = tk.Label(self.master, text="", font=("Helvetica", 12), bg="#f0f0f0")
        self.question_label.pack(pady=10)


        self.timer_label = tk.Label(self.master, text="Time Left: 30", font=("Helvetica", 12), bg="#f0f0f0")
        self.timer_label.pack(pady=5)


        self.answer_buttons = []
        for i in range(4):
            button = tk.Button(self.master, text="", command=lambda i=i: self.submit_answer(i), font=("Helvetica", 12), bg="#2196F3", fg="white")
            button.pack(pady=5)
            self.answer_buttons.append(button)


        self.score_label = tk.Label(self.master, text="Score: 0", font=("Helvetica", 12), bg="#f0f0f0")
        self.score_label.pack(pady=10)

    def start_quiz(self):
        self.score = 0
        self.question_number = 0
        self.fetch_questions()

    def fetch_questions(self):
        category = self.category_var.get()
        difficulty = self.difficulty_var.get()


        category_ids = {
            "General Knowledge": 9,
            "Science: Computers": 18,
            "Entertainment: Books": 10,
            "Entertainment: Film": 11,
            "Entertainment: Music": 12,
        }
        category_id = category_ids.get(category, 9)  
        url = f"https://opentdb.com/api.php?amount=10&category={category_id}&difficulty={difficulty.lower()}&type=multiple"
        response = requests.get(url)
        data = response.json()
        self.questions = data['results']
        self.display_question()

    def display_question(self):
        if self.question_number < len(self.questions):
            question = self.questions[self.question_number]['question']
            self.question_label.config(text=question)

            correct_answer = self.questions[self.question_number]['correct_answer']
            incorrect_answers = self.questions[self.question_number]['incorrect_answers']
            all_answers = incorrect_answers + [correct_answer]
            random.shuffle(all_answers)  


            for i, button in enumerate(self.answer_buttons):
                button.config(text=all_answers[i], state=tk.NORMAL)

            self.time_left = 30 
            self.timer_label.config(text=f"Time Left: {self.time_left}")
            self.start_timer()
        else:
            self.end_quiz()

    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time Left: {self.time_left}")
            self.time_left -= 1
            self.timer = self.master.after(1000, self.start_timer)
        else:
            self.submit_answer(-1) 

    def submit_answer(self, selected_index):
        if self.timer:
            self.master.after_cancel(self.timer)  
        correct_answer = self.questions[self.question_number]['correct_answer']
        if selected_index == -1:

            self.question_label.config(text=f"Time's up! The correct answer was: {correct_answer}")
        else:
            selected_answer = self.answer_buttons[selected_index]['text']
            if selected_answer == correct_answer:
                self.score += 1
                self.question_label.config(text="Correct!")
            else:
                self.question_label.config(text=f"Wrong! The correct answer was: {correct_answer}")

        self.score_label.config(text=f"Score: {self.score}")
        self.question_number += 1
        self.master.after(2000, self.display_question)  

    def end_quiz(self):
        self.question_label.config(text="Quiz Over!")
        self.timer_label.config(text="")
        for button in self.answer_buttons:
            button.config(state=tk.DISABLED)  
        self.start_button.config(state=tk.NORMAL)  
if __name__ == "__main__":
    root = tk.Tk()
    trivia_game = TriviaGame(root)
    root.mainloop()