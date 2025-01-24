import tkinter
import json
import random
from tkinter import ttk
import pygame
from tkinter import messagebox

pygame.mixer.init()

file = open("questions.json", "r", encoding="utf-8")
file = json.load(file)


class AslGame:
    def __init__(self, root, subject):
        self.user_choices = []
        self.user_score = 0
        self.root = root
        self.timer = 13
        self.isRunning = True
        self.subject = subject
        random.shuffle(file[self.subject])
        self.stage_frame = ttk.Frame(self.root, border=5, relief="solid")
        self.stage_frame.place(relx=0.5, x=190, y=10,
                               anchor="ne", width=75, height=30)
        for i in range(4):
            stage = ttk.Label(self.stage_frame, text="   ", background="black")
            stage.place(y=0, x=i * 17)

        self.question_lbl = ttk.Label(
            self.root, justify="center", font=("Arial", 16))
        self.question_lbl.place(relx=0.5, y=51, anchor="n")
        self.options_frame = ttk.Frame(self.root, border=5, relief="solid")
        self.options_frame.place(
            relx=0.5, y=170, height=125, width=325, anchor="center")
        self.timer_lbl = ttk.Label(self.root, font=("Arial", 14))
        self.timer_lbl.place(relx=0.5, x=88, y=12, anchor="nw")
        self.next_button = ttk.Button(
            self.root, text="next", command=self.next_button_func)
        self.question_index = 0
        self.question_loader()
        self.update_timer()

    def question_loader(self):

        for widget in self.options_frame.winfo_children():
            widget.destroy()

        self.question = file[self.subject][self.question_index]["question"]
        self.options = file[self.subject][self.question_index]["options"]
        self.question_lbl.config(text=self.question)
        self.opt1 = ttk.Button(
            self.options_frame, text=self.options[0], command=lambda: self.check_answer(self.options[0]))
        self.opt1.place(relx=0, rely=0)
        self.opt2 = ttk.Button(
            self.options_frame, text=self.options[1], command=lambda: self.check_answer(self.options[1]))
        self.opt2.place(relx=1, rely=0, anchor="ne")
        self.opt3 = ttk.Button(
            self.options_frame, text=self.options[2], command=lambda: self.check_answer(self.options[2]))
        self.opt3.place(relx=0, rely=1, anchor="sw")
        self.opt4 = ttk.Button(
            self.options_frame, text=self.options[3], command=lambda: self.check_answer(self.options[3]))
        self.opt4.place(relx=1, rely=1, anchor="se")

    def update_timer(self):
        if self.isRunning and self.timer > 0:
            self.timer -= 1
            self.timer_lbl.config(
                text=self.timer)
            self.root.after(1000, self.update_timer)
        elif not self.isRunning:
            pass
        else:
            pygame.mixer.Sound("OutOfTime.mp3").play()
            self.isRunning = False
            self.stage_lbl = ttk.Label(
                self.stage_frame, text="   ", background="red")
            self.stage_lbl.place(x=self.question_index*17, y=0)
            self.user_choices.append(
                {"correctness": False, "choice": ""})
            style.configure("Correct.TButton", foreground="green")
            style.configure("Wrong.TButton", foreground="red")
            self.next_button.place(x=0, relx=0.5, y=300, anchor="center")
            for i in [self.opt1, self.opt2, self.opt3, self.opt4]:
                i.config(command=self.idk)

                if i.cget("text") == file[self.subject][self.question_index]["answer"]:
                    i.config(style="Correct.TButton")
                else:
                    i.config(style="Wrong.TButton")

    def check_answer(self, user_option):
        if user_option == file[self.subject][self.question_index]["answer"]:
            self.stage_lbl = ttk.Label(
                self.stage_frame, text="   ", background="green")
            self.stage_lbl.place(x=self.question_index*17, y=0)

            self.user_choices.append(
                {"correctness": True, "choice": user_option})
            self.user_score += 1
            pygame.mixer.Sound("correct.mp3").play()
        else:
            self.stage_lbl = ttk.Label(
                self.stage_frame, text="   ", background="red")
            self.stage_lbl.place(x=self.question_index*17, y=0)

            self.user_choices.append(
                {"correctness": False, "choice": user_option})
            pygame.mixer.Sound("wrong.mp3").play()
        self.isRunning = False
        style.configure("Correct.TButton", foreground="green")
        style.configure("Wrong.TButton", foreground="red")
        self.next_button.place(x=0, relx=0.5, y=300, anchor="center")
        for i in [self.opt1, self.opt2, self.opt3, self.opt4]:
            i.config(command=self.idk)

            if i.cget("text") == file[self.subject][self.question_index]["answer"]:
                i.config(style="Correct.TButton")
            else:
                i.config(style="Wrong.TButton")

    def idk(self):
        pass

    def next_button_func(self,):
        self.question_index += 1
        if self.question_index < 4:
            self.timer = 13
            self.isRunning = True
            self.update_timer()
            self.next_button.place(x=-100, y=-100)
            self.question_loader()
        else:
            for widget in self.root.winfo_children():
                widget.destroy()
            Result(self.root, self.user_choices, self.user_score, self.subject)


class Result:
    def __init__(self, root, choices, score, subject):
        self.root = root
        self.user_choices = choices
        self.user_score = str(score)
        self.question_index = 0
        self.subject = subject
        self.score_lbl = ttk.Label(
            self.root, font=("Arial, 16"), text="your score: "+self.user_score)
        self.score_lbl.place(
            relx=0.5, y=18, anchor="center")
        self.question1 = ttk.Button(self.root, text="first question")
        self.question1.place(
            relx=0.5, y=70, anchor="center", height=35, width=200)
        self.question2 = ttk.Button(self.root, text="second question")
        self.question2.place(
            relx=0.5, y=120, anchor="center", height=35, width=200)
        self.question3 = ttk.Button(self.root, text="third question")
        self.question3.place(
            relx=0.5, y=170, anchor="center", height=35, width=200)
        self.question4 = ttk.Button(self.root, text="fourth question")
        self.question4.place(
            relx=0.5, y=220, anchor="center", height=35, width=200)
        self.next_button = ttk.Button(
            self.root, text="next", command=self.next_button_func)
        self.next_button.place(relx=0.5, y=320, anchor="center")

        style.configure("Correct.TButton", foreground="green")
        style.configure("Wrong.TButton", foreground="red")
        for i in [self.question1, self.question2, self.question3, self.question4]:
            if self.user_choices[self.question_index]["correctness"]:
                i.config(style="Correct.TButton")
            else:
                i.config(style="Wrong.TButton")
            self.question_index += 1

        self.question1.config(command=lambda: messagebox.showinfo(
            "Question 1", file[self.subject][0]["question"] + "\nReal Answer: "+file[self.subject][0]["answer"]+"\nYour Answer: " + self.user_choices[0]["choice"]))
        self.question2.config(command=lambda: messagebox.showinfo(
            "Question 2", file[self.subject][1]["question"] + "\nReal Answer: "+file[self.subject][1]["answer"]+"\nYour Answer: " + self.user_choices[1]["choice"]))
        self.question3.config(command=lambda: messagebox.showinfo(
            "Question 3", file[self.subject][2]["question"] + "\nReal Answer: "+file[self.subject][2]["answer"]+"\nYour Answer: " + self.user_choices[2]["choice"]))
        self.question4.config(command=lambda: messagebox.showinfo(
            "Question 4", file[self.subject][3]["question"] + "\nReal Answer: "+file[self.subject][3]["answer"]+"\nYour Answer: " + self.user_choices[3]["choice"]))

    def next_button_func(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MainMenu(self.root)


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.QoNK_lbl = ttk.Label(
            self.root, text="Quiz Of NoN Kings!", foreground="gray", font=("Chiller", 35))
        self.QoNK_lbl.place(relx=0.5, y=50, anchor="center")
        style.configure("Start.TButton", font=(
            "Arial", 18), foreground="gray")
        self.start_button = ttk.Button(
            self.root, text="Start", style="Start.TButton", command=self.start_func)
        self.start_button.place(
            relx=0.5, y=200, anchor="center", width=120, height=70)

    def start_func(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Subject(self.root)


class Subject:
    def __init__(self, root):
        self.root = root
        self.barnameNevesi = ttk.Button(
            self.root, text="programming", command=lambda: self.button_pressed("barname_nevisi"))
        self.barnameNevesi.place(relx=0.5, x=-80, y=50, anchor="center")
        self.varzeshi = ttk.Button(
            self.root, text="sport", command=lambda: self.button_pressed("varzeshi"))
        self.varzeshi.place(relx=0.5, x=80, y=50, anchor="center")
        self.riyazi = ttk.Button(
            self.root, text="mathemathic", command=lambda: self.button_pressed("riyazi"))
        self.riyazi.place(relx=0.5, x=-80, y=100, anchor="center")
        self.omomi = ttk.Button(
            self.root, text="general", command=lambda: self.button_pressed("omomi"))
        self.omomi.place(relx=0.5, x=80, y=100, anchor="center")
        self.geography = ttk.Button(
            self.root, text="geography", command=lambda: self.button_pressed("geography"))
        self.geography.place(relx=0.5, x=-80, y=150, anchor="center")
        self.history = ttk.Button(
            self.root, text="history", command=lambda: self.button_pressed("history"))
        self.history.place(relx=0.5, x=80, y=150, anchor="center")

    def button_pressed(self, subject):
        for widget in self.root.winfo_children():
            widget.destroy()
        AslGame(self.root, subject)


root = tkinter.Tk()
style = ttk.Style()
style.configure("TButton", font=("Arial", 14))
root.title("QoNK")
root.geometry("410x400")
game = MainMenu(root)
root.mainloop()
