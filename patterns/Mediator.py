
#interface defines the contract for all mediators
class ChatMediator: 
    def sendMessage(self, msg, sender):
        pass

#mediator: handles msg delivery
class DriveShareChat(ChatMediator):
    def __init__(self):
        self.users = []    #list of all registered chat users
    
    # Register a new user so they can send and receive messages
    def registerUser(self,user):
        self.users.append(user)

    # deliver message to all users except the sender
    def sendMessage(self, msg, sender):
        for user in self.users: 
            if user != sender: 
                user.receive(msg, sender)

#colleague: user sends and recieves
class ChatUser: 
    def __init__ (self, name, email, mediator): 
        self.name = name   #displays name 
        self.email = email  #email identifier
        self.chat = mediator  #refrence to mediator
        mediator.registerUser(self)

    #send a message through the mediator to all other users
    def send(self, msg):
        print(f"{self.name} sends: {msg}")
        self.chat.sendMessage(msg, self)

    # receive a message from another user
    def receive(self, msg, sender):
        print(f"{self.name} received a message from {sender.name}: {msg}")
