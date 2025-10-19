import tkinter as tk
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

class SignupWindow:
    def __init__(self, parent, return_callback):
        self.parent = parent
        self.return_callback = return_callback
        self.window = tk.Toplevel(parent)
        self.window.title("Sign Up")
        self.window.geometry("1920x1080")
        
        self.create_widgets()
        self.user_exists = False
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_widgets(self):
        label = tk.Label(self.window, text="Sign Up")
        label.pack(pady=50)

        name_label = tk.Label(self.window, text="Name")
        name_label.pack(pady=10)

        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack(pady=10)

        email_label = tk.Label(self.window, text="Email")
        email_label.pack(pady=10)

        self.email_entry = tk.Entry(self.window)
        self.email_entry.pack(pady=10)
        
        password_label = tk.Label(self.window, text="Password")
        password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack(pady=10)
        
        back_btn = tk.Button(self.window, text="Back", command=self.on_close)
        back_btn.pack(pady=10)

        submit_btn = tk.Button(self.window, text="Submit", command=self.on_submit)
        submit_btn.pack(pady=10)
    
    def on_submit(self):
        # Check if user already exists
        email = self.email_entry.get()
        
        mycursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        existing_user = mycursor.fetchone()
        
        if existing_user:
            if not self.user_exists:
                user_alr_exists_label = tk.Label(self.window, text="User already exists!")
                user_alr_exists_label.pack(pady=20)
                self.user_exists = True

        else:
            name = self.name_entry.get()
            password = self.password_entry.get()
            
            # FIXED: Remove the f-string and use parameterized query correctly
            mycursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                           (name, email, password))
            mydb.commit()
            self.window.withdraw()
            Homepage.Homepagewindow(name, email)

    def on_close(self):
        self.window.destroy()
        self.return_callback()
