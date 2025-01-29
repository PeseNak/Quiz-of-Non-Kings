import tkinter
from tkinter import ttk, messagebox
import json
import random
import pygame

pygame.mixer.init()

qFile = open("data/questions.json", "r", encoding="utf-8")
qData = json.load(qFile)

uFile = open("data/users.json", "r", encoding="utf-8")
uData = json.load(uFile)


class Login_Signin:
    def __init__(self, root):
        self.root = root

        # -------- widgets of login windows --------

        self.QoNK_lbl = ttk.Label(
            self.root, text="Quiz Of NoN Kings!", foreground="gray", font=("Chiller", 35))
        self.QoNK_lbl.place(relx=0.5, y=65, anchor="center")
        self.username_lbl = ttk.Label(
            self.root, text="username:", font=("Arial", 9))
        self.username_lbl.place(relx=0.5, x=-93, y=105,
                                anchor="center")
        self.username_entry = ttk.Entry(
            self.root, font=("Arial", 11), justify="center")
        self.username_entry.place(relx=0.5, y=130, anchor="center", width=250)
        self.password_label = ttk.Label(
            self.root, text="password:", font=("Arial", 9))
        self.password_label.place(relx=0.5, x=-93, y=175, anchor="center")
        self.password_entry = ttk.Entry(
            self.root, show="*", font=("Arial", 11), justify="center")
        self.password_entry.place(relx=0.5, y=200, anchor="center", width=250)
        self.signin_btn = ttk.Button(
            self.root, text="Sign in", command=self.signin)
        self.signin_btn.place(relx=0.5, y=270, anchor="center")
        self.signup_btn = ttk.Button(
            self.root, text="Sign up", command=self.signup)
        self.signup_btn.place(relx=0.5, y=330, anchor="center")
        self.error_lbl = ttk.Label(self.root, font=("Arial", 10))
        self.error_lbl.place(relx=0.5, y=370, anchor="center")

    #  -------- check the entries for Log in --------

    def signin(self):
        if self.username_entry.get() in uData:
            if self.password_entry.get() == uData[self.username_entry.get()]["password"]:
                def login():
                    user = self.username_entry.get()
                    for widget in self.root.winfo_children():
                        widget.destroy()
                    MainMenu(self.root, user)
                self.error_lbl.config(
                    text="loged in", foreground="green")
                self.root.after(1000, login)

            else:
                self.error_lbl.config(
                    text="The password is incorrect", foreground="red")
        else:
            self.error_lbl.config(
                text="No such user exists", foreground="red")

    # -------- check the entries for sign up --------

    def signup(self):
        if self.username_entry.get() in uData:
            self.error_lbl.config(
                text="This username is already taken", foreground="red")
        else:

            uData.update({self.username_entry.get(): {
                "password": self.password_entry.get(), "AllTimeScore": 0}})
            temp2 = open("data/users.json", "w", encoding="utf-8")
            json.dump(uData, temp2, ensure_ascii=False, indent=4)
            temp2.close()
            self.error_lbl.config(
                text="Account created, log in", foreground="green")


class MainMenu:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.userAllScore = uData[self.user]["AllTimeScore"]
        self.QoNK_lbl = ttk.Label(
            self.root, text="Quiz Of NoN Kings!", foreground="gray", font=("Chiller", 35))
        self.QoNK_lbl.place(relx=0.5, y=65, anchor="center")
        style.configure("Start.TButton", font=(
            "Arial", 18), foreground="gray")
        self.user_lbl = ttk.Label(self.root, text=self.user)
        self.user_lbl.place(relx=0.5, x=-150, y=10, anchor="center")
        self.userAllScore_lbl = ttk.Label(self.root, text=self.userAllScore)
        self.userAllScore_lbl.place(relx=0.5, x=160, y=10, anchor="center")
        self.start_button = ttk.Button(
            self.root, text="Start", style="Start.TButton", command=self.start_func)
        self.start_button.place(
            relx=0.5, y=200, anchor="center", width=120, height=70)
        self.suggest_question_btn = ttk.Button(
            self.root, text="Suggest a question", command=self.suggest_func)
        self.suggest_question_btn.place(
            relx=0.5, x=80, y=350, anchor="center")
        self.Logout_btn = ttk.Button(
            self.root, text="Log Out", command=self.logout_func)
        self.Logout_btn.place(relx=0.5, x=-100, y=350, anchor="center")

    def start_func(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Subject(self.root, self.user)

    def suggest_func(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Suggesting(self.root, self.user)

    def logout_func(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Login_Signin(self.root)


class Subject:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        categories = [
            ("programming", 80, -80),
            ("sport", 80, 80),
            ("mathematic", 160, -80),
            ("general", 160, 80),
            ("geography", 240, -80),
            ("history", 240, 80)
        ]
        for text, y, x in categories:
            btn = ttk.Button(
                self.root,
                text=text,
                command=lambda t=text: self.button_pressed(t))
            btn.place(relx=0.5, x=x, y=y, anchor="center")
        self.cancel_btn = ttk.Button(
            self.root, text="cancel", command=self.cancel_func)
        self.cancel_btn.place(relx=0.5, y=340, anchor="center")

    def button_pressed(self, subject):
        for widget in self.root.winfo_children():
            widget.destroy()
        Game(self.root, subject, self.user)

    def cancel_func(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MainMenu(self.root, self.user)


class Game:
    def __init__(self, root, subject, user):
        self.user_choices = []
        self.user_score = 0
        self.root = root
        self.timer = 13
        self.isRunning = True
        self.subject = subject
        self.user = user
        random.shuffle(qData[self.subject])
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

        self.question = qData[self.subject][self.question_index]["question"]
        self.options = qData[self.subject][self.question_index]["options"]
        self.author = qData[self.subject][self.question_index]["author"]
        self.question_lbl.config(text=self.question, wraplength=400)
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

        self.author_lbl = ttk.Label(
            self.root, text=self.author, foreground="gray", font=("Arial", 10))

    def update_timer(self):
        if self.isRunning and self.timer > 0:
            self.timer -= 1
            self.timer_lbl.config(
                text=self.timer)
            self.root.after(1000, self.update_timer)
        elif not self.isRunning:
            pass
        else:
            pygame.mixer.Sound("assets/sounds/timeout.mp3").play()
            self.isRunning = False
            self.stage_lbl = ttk.Label(
                self.stage_frame, text="   ", background="red")
            self.stage_lbl.place(x=self.question_index*17, y=0)
            self.user_choices.append(
                {"correctness": False, "choice": ""})
            style.configure("Correct.TButton", foreground="green")
            style.configure("Wrong.TButton", foreground="red")
            self.next_button.place(x=0, relx=0.5, y=300, anchor="center")
            self.author_lbl.place(x=0, relx=0.5, y=275, anchor="center")
            for i in [self.opt1, self.opt2, self.opt3, self.opt4]:
                i.config(command=self.idk)

                if i.cget("text") == qData[self.subject][self.question_index]["answer"]:
                    i.config(style="Correct.TButton")
                else:
                    i.config(style="Wrong.TButton")

    def check_answer(self, user_option):
        if user_option == qData[self.subject][self.question_index]["answer"]:
            self.stage_lbl = ttk.Label(
                self.stage_frame, text="   ", background="green")
            self.stage_lbl.place(x=self.question_index*17, y=0)

            self.user_choices.append(
                {"correctness": True, "choice": user_option})
            self.user_score += 1
            pygame.mixer.Sound("assets/sounds/correct.mp3").play()
        else:
            self.stage_lbl = ttk.Label(
                self.stage_frame, text="   ", background="red")
            self.stage_lbl.place(x=self.question_index*17, y=0)

            self.user_choices.append(
                {"correctness": False, "choice": user_option})
            pygame.mixer.Sound("assets/sounds/wrong.mp3").play()
        self.isRunning = False
        style.configure("Correct.TButton", foreground="green")
        style.configure("Wrong.TButton", foreground="red")
        self.next_button.place(x=0, relx=0.5, y=300, anchor="center")
        self.author_lbl.place(x=0, relx=0.5, y=275, anchor="center")
        for i in [self.opt1, self.opt2, self.opt3, self.opt4]:
            i.config(command=self.idk)

            if i.cget("text") == qData[self.subject][self.question_index]["answer"]:
                i.config(style="Correct.TButton")
            else:
                i.config(style="Wrong.TButton")

    def idk(self):
        pass

    def next_button_func(self):
        self.question_index += 1
        if self.question_index < 4:
            self.timer = 13
            self.isRunning = True
            self.update_timer()
            self.next_button.place(x=-100, y=-100)
            self.author_lbl.place(x=-100, y=-100)
            self.question_loader()
        else:
            for widget in self.root.winfo_children():
                widget.destroy()
            Result(self.root, self.user_choices,
                   self.user_score, self.subject, self.user)


class Result:
    def __init__(self, root, choices, score, subject, user):
        self.root = root
        self.user = user
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
            "Question 1", qData[self.subject][0]["question"] + "\nReal Answer: "+qData[self.subject][0]["answer"]+"\nYour Answer: " + self.user_choices[0]["choice"]))
        self.question2.config(command=lambda: messagebox.showinfo(
            "Question 2", qData[self.subject][1]["question"] + "\nReal Answer: "+qData[self.subject][1]["answer"]+"\nYour Answer: " + self.user_choices[1]["choice"]))
        self.question3.config(command=lambda: messagebox.showinfo(
            "Question 3", qData[self.subject][2]["question"] + "\nReal Answer: "+qData[self.subject][2]["answer"]+"\nYour Answer: " + self.user_choices[2]["choice"]))
        self.question4.config(command=lambda: messagebox.showinfo(
            "Question 4", qData[self.subject][3]["question"] + "\nReal Answer: "+qData[self.subject][3]["answer"]+"\nYour Answer: " + self.user_choices[3]["choice"]))

        uData[user]["AllTimeScore"] = uData[user]["AllTimeScore"] + \
            int(self.user_score)
        temp1 = open("data/users.json", "w", encoding="utf-8")
        json.dump(uData, temp1, ensure_ascii=False, indent=4)

    def next_button_func(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MainMenu(self.root, self.user)


class Suggesting:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.question_lbl = ttk.Label(
            self.root, text="question:", font=("Arial", 9))
        self.question_lbl.place(relx=0.5, x=-93, y=25,
                                anchor="center")
        self.question_entry = ttk.Entry(
            self.root, font=("Arial", 11), justify="center")
        self.question_entry.place(relx=0.5, y=50, anchor="center", width=250)

        self.options_lbl = ttk.Label(
            self.root, text="options:", font=("Arial", 9))
        self.options_lbl.place(relx=0.5, x=-93, y=90,
                               anchor="center")
        self.opt1 = ttk.Entry(
            self.root, font=("Arial", 11), justify="center")
        self.opt1.place(relx=0.5, y=115, anchor="center", width=250)

        self.opt2 = ttk.Entry(
            self.root, font=("Arial", 11), justify="center")
        self.opt2.place(relx=0.5, y=150, anchor="center", width=250)

        self.opt3 = ttk.Entry(
            self.root, font=("Arial", 11), justify="center")
        self.opt3.place(relx=0.5, y=185, anchor="center", width=250)

        self.opt4 = ttk.Entry(
            self.root, font=("Arial", 11), justify="center")
        self.opt4.place(relx=0.5, y=220, anchor="center", width=250)
        self.category_lbl = ttk.Label(
            self.root, text="category:", font=("Arial", 9))
        self.category_lbl.place(relx=0.5, x=3, y=245,
                                anchor="center")
        self.n = tkinter.StringVar()
        self.subject = ttk.Combobox(
            self.root, state="readonly", textvariable=self.n)
        self.subject['values'] = (
            'programming', 'sport', 'mathematic', 'general', 'geography', 'history')
        self.subject.place(x=51, relx=0.5, y=270, anchor="center")
        self.correct_opt_lbl = ttk.Label(
            self.root, text="correct option:", font=("Arial", 9))
        self.correct_opt_lbl.place(relx=0.5, x=-88, y=245,
                                   anchor="center")
        self.m = tkinter.StringVar()
        self.correct_opt = ttk.Combobox(
            self.root, state="readonly", textvariable=self.m)
        self.correct_opt['values'] = (1, 2, 3, 4)
        self.correct_opt.place(x=-87, relx=0.5, y=270,
                               anchor="center", width=75)
        self.sub_button = ttk.Button(
            self.root, text="submit", command=self.suggest_func)
        self.sub_button.place(relx=0.5, y=335, anchor="center")
        self.sub_lbl = ttk.Label(self.root, font=("Arial", 10))
        self.sub_lbl.place(relx=0.5, y=300, anchor="center")

        self.cancel_btn = ttk.Button(
            self.root, text="cancel", command=self.cancel_func)
        self.cancel_btn.place(relx=0.5, y=380, anchor="center")

    def suggest_func(self):
        for i in [self.m.get(), self.n.get(), self.opt1.get(), self.opt2.get(), self.opt3.get(), self.opt4.get(), self.question_entry.get()]:
            if i == "":
                messagebox.showerror("error", "fill all the sections")
                break
        else:
            options = [self.opt1.get(), self.opt2.get(),
                       self.opt3.get(), self.opt4.get()]
            file = open("data/userQ.json", "r", encoding="utf-8")
            userQR = json.load(file)
            userQR[self.n.get()].append({
                "question": self.question_entry.get(),
                "options": options,
                "answer": options[int(self.m.get()) - 1],
                "author": self.user
            })
            userQW = open("data/userQ.json", "w", encoding="utf-8")
            json.dump(userQR, userQW, ensure_ascii=False, indent=4)
            userQW.close()

            def idk():
                for widget in self.root.winfo_children():
                    widget.destroy()
                MainMenu(self.root, self.user)
            self.sub_lbl.config(
                text="Sent to admin", foreground="green")
            self.root.after(1000, idk)

    def cancel_func(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MainMenu(self.root, self.user)


root = tkinter.Tk()
style = ttk.Style()
style.configure("TButton", font=("Arial", 14))
root.title("QoNK")

root.geometry("410x400+550+250")
game = Login_Signin(root)
root.resizable(False, False)
root.mainloop()
qFile.close()
uFile.close()
