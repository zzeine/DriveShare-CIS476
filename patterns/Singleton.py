
class User: 
    def __init__(self, email, password, security_questions): 
        self.email = email 
        self.password = password
        self.security_questions = security_questions


class SessionManager: 
    #static variable to hold ONE instance 
    __instance = None

    def __init__(self):
        #private constructors:
        self.users = [] #list of users
        self.currentUser = None # store logged in user 

    @staticmethod
    def getInstance():
        #check if instance exists if not create one 
        if SessionManager.__instance is None: 
            SessionManager.__instance = SessionManager()
        return SessionManager.__instance
    #add new users 
    def register(self, user):
        self.users.append(user)
    #authenticate user by checking email and password
    def login(self, email, password):
        for user in self.users: 
            if user.email == email and user.password == password: 
                self.currentUser = user
                print ("Login Successful!")
                return 
        print("Invalid email or password")
        return 
    #delete current session
    def logout(self):
        self.currentUser = None 
        print("Logged out successfully!")
    #return currently logged in user 
    def getCurrentUser(self): 
        return self.currentUser
    
    

