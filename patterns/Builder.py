#product
class CarListing:
    def __init__(self):
        self.model = None
        self.year = None
        self.mileage = None
        self.pricePerDay = None
        self.color = None
        self.transmission = None
        self.fuelType = None
        self.features = []
        self.pickupLocation = None

    def __str__(self):
        return f"{self.year} {self.model} - ${self.pricePerDay}/day"
    
#builder 
class CarListingBuilder:
    def __init__(self):
        self.car = CarListing()

    def setModel(self, model):
        self.car.model = model
        return self

    def setYear(self, year):
        self.car.year = year
        return self

    def setMileage(self, mileage):
        self.car.mileage = mileage
        return self

    def setPrice(self, price):
        self.car.pricePerDay = price
        return self

    def setPricePerDay(self, price):
        self.car.pricePerDay = price
        return self

    def setColor(self, color):
        self.car.color = color
        return self

    def setTransmission(self, transmission):
        self.car.transmission = transmission
        return self

    def setFuelType(self, fuel):
        self.car.fuelType = fuel
        return self

    def addFeature(self, feature):
        self.car.features.append(feature)
        return self

    def setPickupLocation(self, location):
        self.car.pickupLocation = location
        return self

    def build(self):
        return self.car
    
#director
class CarListingDirector:
    def constructBasicListing(self, builder):
        return (builder
                .setModel("Toyota Camry")
                .setYear(2020)
                .setMileage(30000)
                .setPrice(45)
                .build())

    def constructFullListing(self, builder):
        return builder.build()