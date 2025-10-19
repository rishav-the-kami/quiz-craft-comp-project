import tkinter as tk
from tkinter import ttk
import mysql.connector
import Homepage

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="p@$$word12",
    database="quiz-craft-db",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

print("Connection successful")

class Leaderboard():
    def __init__(self):
        mycursor.execute("select sum(score), id from scores group by id ORDER BY SUM(SCORE) DESC")
        data = mycursor.fetchall()
        self.window = tk.Tk()
        self.window.geometry('1920x1080')
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

        for i in data:
            mycursor.execute(f"select name from users where email = '{i[1]}'")
            name = (mycursor.fetchone())[0]

            # Create a frame (container) with border and make it clickable
            container = tk.Frame(self.inner_frame, relief="solid", borderwidth=1, padx=10, pady=10)
            container.pack(fill="both", expand=True, padx=20, pady=20)

            # Add labels to the container
            label_left = tk.Label(container, text=name)
            label_left.pack(side="left")

            label_right = tk.Label(container, text=str(i[0]))
            label_right.pack(side="right")
            

            