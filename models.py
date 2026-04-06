from datetime import datetime

#user
class User: 
    def __init__(self, email, password, securityQuestions): 
        #basic user info 
        self.email = email 
        self.password = password
        self.securityQuestions = securityQuestions #list of 3 answers for password recovery
    def login(self): return True
    def recoverPassword(self): return True

#Owner user who lists and manages cars for rent
class Owner(User): 
    def __init__(self, email, password, securityQuestions):
        super().__init__(email, password, securityQuestions)
        self.cars= []    #list of owned cars
        self.bookings = []  #list of bookings for cars

    #add a car to the owners list
    def listCar(self, car): 
        self.cars.append(car) 

    # update car details
    def updateCar(self, car): 
        pass

    # return all bookings for this owners cars
    def viewbookings(self): 
        return self.bookings

#Renter user who searches and books cars
class Renter(User): 
    def __init__(self, email, password, securityQuestions):
        super().__init__(email, password, securityQuestions)
        self.watchlist = []  
    # search for cars based on criteria
    def searchCars(self, criteria):
        return []
    #create and return a booking for a car
    def bookCar(self, car, startDate, endDate):
        return Booking(0, car, self, startDate, endDate)
    
    #add a car to the renters watchlist with a price threshold
    def addToWatchlist(self, car, priceThreshold):
        self.watchlist.append(WatchList(0, self, car, priceThreshold))

#car 
class Car: 
    def __init__(self, carID, model, year, mileage, pickupLocation, pricePerDay, availabilityCalender, ownerID): 
        self.carID = carID
        self.model = model 
        self.year = year
        self.mileage = mileage
        self.pickupLocation = pickupLocation
        self.pricePerDay = pricePerDay
        self.availabilityCalender = availabilityCalender
        self.ownerId = ownerID
        self.observers = []  #list of renters watching this car 

    #add a renter to the observer list
    def attach(self, renter):   
        self.observers.append(renter)

    #remove a renter from the observer list    
    def detach(self, renter):   
        if renter in self.observers:
            self.observers.remove(renter)

    #notify all watching renters of a change
    def notify(self):           
        for renter in self.observers:
            renter.update(self)

    #update price and notify all observers
    def updatePrice(self, newPrice):    
        self.pricePerDay = newPrice
        self.notify()    

    # check if car is available for given dates
    def isAvailable(self, startDate, endDate): 
        return True 
    
    def updateAvailability(self, startDate, endDate): 
        self.availabilityCalender[(startDate, endDate)] = "booked"
  

#bookings links renter and car for specific date range
class Booking: 
    def __init__(self, bookingID, car, renter, startDate, endDate):
        self.bookingID = bookingID
        self.car = car
        self.renter = renter
        self.startDate = startDate
        self.endDate = endDate
        self.totalPrice = self.calculateTotalPrice()

    #calculate total cost based on number of days and price per day
    def calculateTotalPrice(self):
        days = (self.endDate - self.startDate).days
        return days * self.car.pricePerDay   #days *priceperday

    #print booking confirmation
    def confirmBooking(self):
        print(f"Booking confirmed for {self.renter.email} on {self.car.model}")

#payment 
class Payment:
    def __init__(self, paymentID, booking, payer, payee, amount):
        self.paymentID = paymentID
        self.booking = booking
        self.payer = payer   #renter
        self.payee = payee   #owner
        self.amount = amount
        self.status = "Pending"
    #process the payment and mark completed
    def makePayment(self):
        print(f"Processing payment of ${self.amount} from {self.payer.email} to {self.payee.email}")
        self.status = "Completed"

    def updateStatus(self, newStatus):
        self.status = newStatus

#watchlist 
class WatchList:
    def __init__(self, watchID, renter, car, priceThreshold):
        self.watchID = watchID
        self.renter = renter
        self.car = car
        self.priceThreshold = priceThreshold
    #attach renter as observer to car
    def addWatch(self):
        self.car.attach(self.renter)  # registers renter as observer
        print(f"{self.renter.email} is watching {self.car.model} at ${self.priceThreshold}")
    #notify renter when price droped
    def notifyRenter(self):
        print(f"Notification → {self.renter.email}: {self.car.model} dropped below ${self.priceThreshold}")

#message
class Message:
    def __init__(self, messageID, sender, receiver, content):
        self.messageID = messageID
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = datetime.now()

    def sendMessage(self):
        print(f"{self.sender.email} -> {self.receiver.email}: {self.content}")

    def readMessage(self):
        print(f"[{self.timestamp}] {self.content}")