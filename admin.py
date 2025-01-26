import tkinter
from tkinter import ttk, messagebox
import json

file = open("data/userQ.json", "r", encoding="utf-8")
questions_data = json.load(file)
file = open("data/questions.json", "r", encoding="utf-8")
accepted_questions = json.load(file)


def save_changes():
    file = open("data/userQ.json", "w", encoding="utf-8")
    json.dump(questions_data, file, ensure_ascii=False, indent=4)

    file = open("data/questions.json", "w", encoding="utf-8")
    json.dump(accepted_questions, file, ensure_ascii=False, indent=4)


class Review:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Question Review")
        self.root.geometry("410x400+550+250")
        self.category_lbl = ttk.Label(
            self.root, wraplength=400, font=("Arial", 14), justify="center")
        self.category_lbl.place(relx=0.5, anchor="center", y=15)
        self.question_lbl = ttk.Label(
            self.root, wraplength=400, font=("Arial", 14), justify="center"
        )
        self.question_lbl.place(relx=0.5, anchor="center", y=60)
        self.options_lbl = ttk.Label(
            self.root, wraplength=400, font=("Arial", 14), justify="center"
        )
        self.options_lbl.place(relx=0.5, anchor="center", y=150)
        self.author_lbl = ttk.Label(
            self.root, wraplength=400, font=("Arial", 10), justify="center", foreground="gray"
        )
        self.author_lbl.place(relx=0.5, anchor="center", y=250)
        self.answer_lbl = ttk.Label(
            self.root, wraplength=400, font=("Arial", 14), justify="center", foreground="lime"
        )
        self.answer_lbl.place(relx=0.5, anchor="center", y=285)

        self.accept_btn = ttk.Button(
            self.root, text="Accept", command=self.accept_question
        )
        self.accept_btn.place(relx=0.5, x=-100, anchor="center", y=320)

        self.reject_btn = ttk.Button(
            self.root, text="Reject", command=self.reject_question
        )
        self.reject_btn.place(relx=0.5, x=100, anchor="center", y=320)

        self.current_category = None
        self.current_index = 0
        self.load_next_question()

    def load_next_question(self):
        for category, questions in questions_data.items():
            if questions:
                self.current_category = category
                self.current_question = questions[0]
                self.update_question_display()
                return

        messagebox.showinfo("Done", "No more questions to review.")
        save_changes()
        self.root.destroy()

    def update_question_display(self):
        question_text = self.current_question["question"]
        author_text = self.current_question["author"]
        answer_text = self.current_question["answer"]
        options_text = ""
        option_numbers = range(1, 5)
        for number, option in zip(option_numbers, self.current_question["options"]):
            options_text += str(number) + ". " + option + "\n"
        self.question_lbl.config(text=question_text)
        self.category_lbl.config(text="Category: " + self.current_category)
        self.options_lbl.config(text="\nOptions:\n" + options_text)
        self.answer_lbl.config(text="Answer: " + answer_text)
        self.author_lbl.config(text=author_text)

    def accept_question(self):
        accepted_questions[self.current_category].append(self.current_question)
        questions_data[self.current_category].pop(0)
        self.load_next_question()

    def reject_question(self):
        questions_data[self.current_category].pop(0)
        self.load_next_question()


root = tkinter.Tk()
app = Review(root)
root.mainloop()
