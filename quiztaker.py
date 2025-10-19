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

    class Quiztaker:
        def __init__(self, root, name, user_id, quiz_id):
            self.name=name
            self.user_id = user_id
            self.quiz_id = quiz_id
            self.questions = []
            self.current_question = 0

            self.score = 0

            self.window = tk.Toplevel(root)
            self.window.geometry("1920x1080")

            self.question_label = tk.Label(self.window, text="Question 1:")
            self.question_label.pack()
            
            mycursor.execute(f"SELECT * FROM quizzes WHERE id = {str(self.quiz_id)}")
            self.data = mycursor.fetchall()

            self.counter = 0
            self.options = eval(self.data[0][2])

            self.question = tk.Label(self.window, text=self.data[self.counter][1])
            self.question.pack()

            self.option1 =  tk.Label(self.window, text=str((1))+" "+self.options[0])
            self.option2 =  tk.Label(self.window, text=str((2))+" "+self.options[1])
            self.option3 =  tk.Label(self.window, text=str((3))+" "+self.options[2])
            self.option4 =  tk.Label(self.window, text=str((4))+" "+self.options[3])

            answer_entry = tk.Entry(self.window)
            answer_entry.pack()

            submit_button = tk.Button(self.window, text="Submit", command=lambda: self.on_submit(self.data[0][3], answer_entry.get()))
            submit_button.pack()

            self.option1.pack()
            self.option2.pack()
            self.option3.pack()
            self.option4.pack()

            self.window.mainloop()


        def on_submit(self, correct_option, selected_option):
            if int(selected_option)-1 == int(correct_option):
                print("CORRECT")
                self.score += 1
                
            else:
                print("INCORRECT")

            if self.counter < 3:
                self.counter += 1
                self.options=eval(self.data[self.counter][2])
                self.question_label.config(text="Question: "+str(self.counter+1))
                self.question.config(text=self.data[self.counter][1])
                self.option1.config(text="1 "+self.options[0])
                self.option2.config(text="2 "+self.options[1])
                self.option3.config(text="3 "+self.options[2])
                self.option4.config(text="4 "+self.options[3])
            else:
                print("EnD REACHED!")
                mycursor.execute("INSERT INTO scores(id, score, name) VALUES(%s, %s, %s)", (self.user_id, self.score+1, self.name))
                print("Successfully updated Leaderboard")
                mydb.commit()

                score_label = tk.Label(self.window, text="Your score is: " + (str(self.score+1)))
                score_label.pack()

                
except Exception as e:

    print(e)

