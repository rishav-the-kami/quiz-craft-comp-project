import tkinter as tk
import mysql.connector
import Homepage

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="p@$$word12",
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

            
            # print("in quiztaker:", self.user_id, self.name, self.quiz_id)
            
            # self.option_entries = []
            # for i in range(4):
            #     label = tk.Label(self.window, text=f"Option {i+1}:")
            #     label.pack()
            #     entry = tk.Entry(self.window)
            #     entry.pack()
            #     self.option_entries.append(entry)
            
            # self.correct_var = tk.IntVar()
            # self.correct_label = tk.Label(self.window, text="Correct option (1-4):")
            # self.correct_label.pack()
            # self.correct_entry = tk.Entry(self.window)
            # self.correct_entry.pack()
            
            # self.next_button = tk.Button(self.window, text="Next", command=self.next_question)
            # self.next_button.pack()

        

        # def next_question(self):
        #     question = self.question_entry.get()
        #     options = [entry.get() for entry in self.option_entries]
        #     correct = int(self.correct_entry.get()) - 1
            
        #     self.questions.append((question,str(options),correct))

        #     mycursor.execute("INSERT INTO quizzes(qno, question, options, correct, created_by, id) VALUES (%s, %s,%s,%s, %s, %s)", (self.current_question, question, str(options),correct, self.name, self.no_of_quizzes))
        #     print("Added Question", self.current_question)
            
        #     self.current_question += 1
            
        #     if self.current_question < 4:
        #         self.question_label.config(text=f"Question {self.current_question + 1}:")
        #         self.question_entry.delete(0, tk.END)
        #         for entry in self.option_entries:
        #             entry.delete(0, tk.END)
        #         self.correct_entry.delete(0, tk.END)
        #     else:
        #         print("Quiz creation complete!")
        #         print(self.questions)
        #         mydb.commit()

        #         self.window.withdraw()
        #         Homepage.Homepagewindow(self.name, self.user_id)
                
except Exception as e:
    print(e)