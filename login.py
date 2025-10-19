import tkinter as tk
from tkinter import ttk
import Homepage
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password for sql",
    database="quiz-craft-db",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

print("Connection succcessful")

class LoginWindow:
    def __init__(self, parent, return_callback):
        print("in login page")
        self.parent = parent
        self.return_callback = return_callback
        self.window = tk.Toplevel(parent)
        self.window.title("Login")
        self.window.geometry("1920x1080")

        self.user_not_exist_displayed = False
        
        self.create_widgets()
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_widgets(self):
        label = tk.Label(self.window, text="Login")
        label.pack(pady=50)

        email_label = tk.Label(self.window, text="Email")
        email_label.pack(pady=50)

        self.email_entry = tk.Entry(self.window)
        self.email_entry.pack(pady=50)
        
        password_label = tk.Label(self.window, text="Password")
        password_label.pack(pady=50)

        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack(pady=50)
        back_btn = tk.Button(self.window, text="Back", command=self.on_close)
        back_btn.pack()

        submit_btn = tk.Button(self.window, text="Submit", command=self.on_submit)
        submit_btn.pack()

    def on_submit(self):
        mycursor.execute(f"SELECT name FROM users WHERE email = '{self.email_entry.get()}' AND password='{self.password_entry.get()}'")
        name = mycursor.fetchone()
        print("NAME:", name)

        mycursor.execute("SELECT email,password FROM users")
        data = mycursor.fetchall()
        if (self.email_entry.get(), self.password_entry.get()) in data:
            self.window.withdraw()
            Homepage.Homepagewindow(name[0],self.email_entry.get())
        else:
            if not self.user_not_exist_displayed:
                user_no_exist_label = tk.Label(self.window, text="User Doesnt Exist!")
                user_no_exist_label.pack(pady=20)
                self.user_not_exist_displayed = False

    def on_close(self):
        self.window.destroy()

        self.return_callback()

