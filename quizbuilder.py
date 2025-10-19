import tkinter as tk
import mysql.connector
import Homepage

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password for sql",
        database="quiz-craft-db",
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    print("Connection successful")

    class QuizMaker:
        def __init__(self, root, name, id):
            self.name=name
            self.questions = []
            self.id = id
            self.current_question = 0

            self.window = tk.Toplevel(root)
            self.window.geometry("1920x1080")

            self.question_label = tk.Label(self.window, text="Question 1:")
            self.question_label.pack()
            
            self.question_entry = tk.Entry(self.window)
            self.question_entry.pack()
            
            mycursor.execute("SELECT COUNT(*) FROM quizzes GROUP BY id")
            self.no_of_quizzes = len(mycursor.fetchall())
            print("length: ", self.no_of_quizzes)
            
            self.option_entries = []
            for i in range(4):
                label = tk.Label(self.window, text=f"Option {i+1}:")
                label.pack()
                entry = tk.Entry(self.window)
                entry.pack()
                self.option_entries.append(entry)
            
            self.correct_var = tk.IntVar()
            self.correct_label = tk.Label(self.window, text="Correct option (1-4):")
            self.correct_label.pack()
            self.correct_entry = tk.Entry(self.window)
            self.correct_entry.pack()
            
            self.next_button = tk.Button(self.window, text="Next", command=self.next_question)
            self.next_button.pack()

            self.window.mainloop()

        def next_question(self):
            question = self.question_entry.get()
            options = [entry.get() for entry in self.option_entries]
            correct = int(self.correct_entry.get()) - 1
            
            self.questions.append((question,str(options),correct))

            mycursor.execute("INSERT INTO quizzes(qno, question, options, correct, created_by, id) VALUES (%s, %s,%s,%s, %s, %s)", (self.current_question, question, str(options),correct, self.name, self.no_of_quizzes))
            print("Added Question", self.current_question)
            
            self.current_question += 1
            
            if self.current_question < 4:
                self.question_label.config(text=f"Question {self.current_question + 1}:")
                self.question_entry.delete(0, tk.END)
                for entry in self.option_entries:
                    entry.delete(0, tk.END)
                self.correct_entry.delete(0, tk.END)
            else:
                print("Quiz creation complete!")
                print(self.questions)
                mydb.commit()

                self.window.withdraw()
                Homepage.Homepagewindow(self.name, self.id)
                
except Exception as e:

    print(e)
