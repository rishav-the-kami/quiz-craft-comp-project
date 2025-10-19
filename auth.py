import tkinter as tk
import login
import signup

class AuthenticationWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Authentication")
        self.root.geometry("300x200")
        
        login_btn = tk.Button(self.root, text="Login", command=self.open_login)
        login_btn.pack(pady=10)
        
        signup_btn = tk.Button(self.root, text="Sign Up", command=self.open_signup)
        signup_btn.pack(pady=10)
    
    def open_login(self):
        self.root.withdraw()
        login.LoginWindow(self.root, self.show_auth_window)
    
    def open_signup(self):
        self.root.withdraw()
        signup.SignupWindow(self.root, self.show_auth_window)
    
    def show_auth_window(self):
        self.root.deiconify()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AuthenticationWindow()
    app.run()