
class Car:
    def __init__(self, model, pricePerDay, availability=True):
        self.model = model 
        self.pricePerDay = pricePerDay
        self.availability = availability
        self.observers = [] #list of renters watching car

    #add renter to observer list 
    def attach(self, renter):
        self.observers.append(renter)

    #remove renter from list
    def detach(self, renter):
        if renter in self.observers:
            self.observers.remove(renter)
    
    #notify all renters watching the car 
    def notify(self):
        for renter in self.observers: 
            renter.update(self)
    
    #update price and notify renters
    def updatePrice(self, newPrice): 
        self.pricePerDay = newPrice
        print(f"Price updated for {self.model} to ${newPrice}")
        self.notify()
    
    #update availabilty and notify renters
    def updateAvailability(self, status):
        self.availability = status
        print(f"Avalability updated for {self.model}: {status}")
        self.notify()

class Renter: 
    def __init__(self, name, email):
        self.name = name
        self.email = email 
    #start watching car
    def watchCar(self, car): 
        car.attach(self)
        print(f"{self.name} is now watching {car.model}")

    #get notifications from car
    def update(self, car):
        print(f"Notification for {self.name}: {car.model} has been updated!")
        print(f"New price: ${car.pricePerDay}, Availability: {car.availability}")




        

