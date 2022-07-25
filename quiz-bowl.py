from api_functions import *
from helpful_tools import *
from time import sleep


class User():

    def __init__(self, user_info):
        self.user_info = user_info
        self.score = 0
        self.quiz = []
        self.name = self.user_info['first_name'].title()
        self.token = self.user_info['token']
        self.missed = []

    def update(self):
        self.userinfo = login_user(self.user_info['email'],'123')
    
    def take_quiz(self):
        n = 1
        for q in self.quiz:
            missed = {}
            clear()
            print(f"Question #{n}:")
            print(f"Authored By: {q['author']}")
            print(q['question'])
            answer = input("You're answer: ")
            if check_answer(answer, q['answer']): #Thoroughly checks your answer to see if it's correct
                self.score += 1
            else:
                missed = {
                    'number': n,
                    'question': q['question'],
                    'right': q['answer'],
                    'wrong': answer
                }
                self.missed.append(missed)
            n += 1
            print(f"Recording answer: {answer}")
            sleep(1.5)
        #iterates over the quiz list prints question
        #asks for answer
        #evaluates if answer is true or false
        #if true, increments the score


    def set_quiz(self):
        self.missed = []
        self.quiz = get_quiz(self.token)

    def display_score(self):
        print(f"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        You scored: {self.score}/10""")
        if self.score < 5:
            print(f"\tYou're kinda dumb, aren't you {self.name}?")
        elif self.score > 7:
            print("\tLook at you smarty pants!")
        else:
            print(f"\tNot too shabby {self.name}.")
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        if self.missed:
            print("Here is what you missed: ")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            for q in self.missed:
                print(f"""
Question #{q['number']}
{q['question']}
You answered: {q['wrong']}
The correct answer was: {q['right']}\n
                """)
        input("press Enter to continue")

class Admin(User):

    def __init__ (self, user_info):
        super().__init__(user_info)
        self.score = 0
        self.quiz = []
        self.name = self.user_info['first_name']
        self.token = self.user_info['token']

        #We get all the quiz functions from User()
        
    @property
    def my_questions(self):
        return get_all_admin_questions(self.token)

    def create_question(self):
        print("To leave, answer 'back' to any question")
        question = input("What question would you like to add?: ").lower()
        if question == 'back':
            return
        answer = input("What is the answer?: ")
        if answer == 'back':
            return
        payload = {
            "question": question,
            "answer": answer
        }
        response = create_a_question(self.token, payload)
        self.update()
        return response
        #Gets question and answer from admin
        #creates payload
        #calls api post function to create the question with admin token and payload
        #returns success <id> created
        

    def edit_question(self):
        while True:
            clear()
            self.display_my_questions()
            id = int(input("Select the question you'd like to edit using the question ID: "))
            q = get_question(id, self.my_questions)
            if q: 
                q = q[0]
                while True:
                    clear()
                    print(f"Selected Question: {q['question']}")
                    print(f"Answer: {q['answer']}\n")
                    edit = input("Would you like to edit the question, answer, both, or quit? ").lower()
                    if edit == "quit": return
                    if edit == 'question':
                        question = input("What would you like to change the question to?: ")
                        payload = {
                        "question": question
                        }
                        break
                    elif edit == 'answer':
                        answer = input("What would you like to change the answer to?: ")
                        payload = {
                        "answer": answer
                        }
                        break
                    elif edit == 'both':
                        question = input("What would you like to change the question to?: ")
                        answer = input("What would you like to change the answer to?: ")
                        payload = {
                        "question": question,
                        "answer": answer
                        }
                        break
                    else:
                        print("Invalid Selection!")
                        sleep(2)
                break
            else:
                print("Invalid question ID!")
                sleep(2)
        success = edit_specific_question(self.token, payload, id)
        self.update()
        if success:
            print("Question successfully edited!")
        else:
            print("Somthing went wrong, please try again")
        #if admin is writer of question, they are asked if they want to edit the question
        #the answer or both, a payload is created and sent to api edit function
        

    def delete_question(self):
        while True:
            clear()
            self.display_my_questions()
            id = int(input("Select they question you wish to delete using the question ID: "))
            q = get_question(id, self.my_questions)
            if q:
                q = q[0]
                print(f"\nSelected Question: {q['question']}")
                print(f"Answer: {q['answer']}\n")
                delete = input("Are you sure you would like to delete this question?: (Y/N)").lower()
                if delete == 'y':
                    delete_question(self.token, id)
                    self.update()
                    print("Question successfully deleted")
                    sleep(2)
                    return
                elif delete == 'n':
                    different = input("Is there another question you would like to delete? (Y/N)").lower()
                    if different == 'y':
                        break
                    else:
                        return
            else:
                print("Invalid ID Selection!")
                sleep(2)
                        
        #verifies admin is the creator of the question
        #If they are sends token to delete api function
    
    def display_my_questions(self):
        print("The Questions you've written:\n")
        for q in self.my_questions:
            print(f'Question: {q["question"]}')
            print(f'Answer: {q["answer"]}')
            print(f'ID : {q["id"]}')
            print('\n'+'~'*50+'\n')
        


class UI:

    def __init__(self):
        self.user = None
        self.admin = None

    def login(self, email):
        clear()
        password=input("Password: ")
        user = login_user(email, password) 
        return user

    def register(self):
        clear()
        print("Registration:")
        email = input("Email: ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        password = input("Password: ")

        user_dict={
            "email":email,
            "first_name":first_name,
            "last_name":last_name,
            "password":password
        }
        return register_user(user_dict)


    def main(self):
        clear()
        while True:
            print("Welcome to the 20301 annual super quiz bowl-o-rama")
            email = input("Login ith email or type 'register' to create and account: ").lower()
            if email == "register":
                success_register= self.register()
                if success_register:
                    print("You have successfully registered")
                    continue
            elif email.lower() == "quit":
                print("Goodbye")
                break
            else:
                try:
                    user_info = self.login(email)
                    break
                except:
                    print("Invalid Username/Password combo")
                    sleep(2)
                    continue

        
        if user_info['admin']:
            self.user = Admin(user_info)
            self.admin = True
        else:
            self.user = User(user_info)

        if self.admin:
            while True:
                clear()
                print(f"""
    Welcome Back {self.user.name}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. See Your Questions
2. Add Question
3. Edit a Question
4. Delete a Question
5. Take a Quiz
6. Quit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            """)
                action = input("Select an action: ")
                if action == '1':
                    self.user.display_my_questions()
                    input("Press Enter to return.")
                elif action == '2':
                    print(self.user.create_question())
                    sleep(1.5)
                elif action == '3':
                    self.user.edit_question()
                elif action == '4':
                    self.user.delete_question()
                elif action == '5':
                    self.user.set_quiz()
                    self.user.take_quiz()
                    self.user.display_score()
                elif action == '6':
                    break
                else:
                    print("Invalid Selection, try again Idiot!")
                    sleep(2)
        
        else:
            print(f'\n\n\t\tWelcome to the Quiz Bowl {self.user.name}')
            input("\t\t--Press enter to start your quiz!--")
            while True:
                self.user.set_quiz()
                self.user.take_quiz()
                self.user.display_score()
                again = input("Would you like to take another quiz? (Y/N): ").lower()
                if again == 'n':
                    print("Have a Nice Day!")
                    break
                print("Awesome ret ready for your next round!")
                sleep(2)
        
        print("Program Ended")

if __name__ == '__main__':
    UI().main()


                
                
