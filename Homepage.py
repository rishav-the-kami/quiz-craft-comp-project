import tkinter as tk
import quizbuilder
import quiztaker
import mysql.connector
import leaderboard
from tkinter import ttk

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password for sql",
        database="quiz-craft-db",
        auth_plugin='mysql_native_password'
    )

mycursor = mydb.cursor()

print("Connection successful")

class Homepagewindow:
    def __init__(self, name, id):
        self.name = name
        self.window = tk.Tk()
        self.id = id
        self.window.geometry("1920x1080")
        text = tk.Label(self.window, text="Homepage")
        text.pack()

        print("Hi", self.name)

        quiz_builder_btn = tk.Button(self.window, text="Build your own Quiz", command=self.open_quiz_builder)
        quiz_builder_btn.pack()
        
        leaderboard_btn = tk.Button(self.window, text="Leaderboard", command=self.open_leaderboard)
        leaderboard_btn.pack()

        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbar to canvas
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create another frame inside canvas
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.display_quizzes()

    def display_quizzes(self):
        mycursor.execute("select COUNT(*), id, created_by FROM quizzes GROUP BY id, created_by")
        data = mycursor.fetchall()

        d={}

        for i in data:
            print(i)
            d[i[1]] = ["Created by:"+i[2], "Questions:"+str(i[0])] 

        for k,v in d.items():
            print("key,value",k,v)
            clickable_area = tk.Button(
                self.inner_frame,
                command=lambda idx=k: self.on_click(idx),
                relief="solid",
                text=v[0],
                bg="white",
                height=5,
                width=40,
                borderwidth=3,
                pady=5
            )

            clickable_area.pack()

        

    def open_leaderboard(self):
        self.window.withdraw()
        leaderboard.Leaderboard()
    def on_click(self, id):
        print(id)
        self.window.withdraw()
        quiztaker.Quiztaker(self.window, self.name, self.id, id)

    def open_quiz_builder(self):
        self.window.withdraw()

        quizbuilder.QuizMaker(self.window, self.name, self.id)
