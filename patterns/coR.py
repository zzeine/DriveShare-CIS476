
# base handler
class SecurityQuestionHandler:
    def __init__(self, correctAnswer):
        self.correctAnswer = correctAnswer
        self.nextHandler = None

    #set next handler in the chain
    def setNext(self, handler):
        self.nextHandler = handler
        return handler  

    # Handle the user's answer
    def handle(self, answer):
        #check that  answer matches
        if answer != self.correctAnswer:
            print("Incorrect answer. Password recovery failed.")
            return False
        print("Correct answer.")
        return True

    
#conctrete handler 1
class Question1Handler(SecurityQuestionHandler):
    def ask(self):
        answer = input("Security Question 1: What is your favorite color? ")
        return self.handle(answer)
    
#conctrete handler 2
class Question2Handler(SecurityQuestionHandler):
    def ask(self):
        answer = input("Security Question 2: What city were you born in? ")
        return self.handle(answer)

#conctrete handler 3
class Question3Handler(SecurityQuestionHandler):
    def ask(self):
        answer = input("Security Question 3: What is your mom's name? ")
        return self.handle(answer)
