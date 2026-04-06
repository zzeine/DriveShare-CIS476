from datetime import date

from models import User, Owner, Renter, Car, Booking, Payment, Message, WatchList

from patterns.Singleton import SessionManager
from patterns.Observer import Car as obsCar, Renter as obsRenter
from patterns.Mediator import DriveShareChat, ChatUser
from patterns.Builder  import CarListingBuilder, CarListingDirector
from patterns.Proxy import PaymentProxy
from patterns.coR import Question1Handler, Question2Handler, Question3Handler

# hardcoded users and cars for testing
def initialize_data():
    # owners
    owner1 = Owner("ali@google.com", "1111", ["blue", "detroit", "luna"])
    owner2 = Owner("maria@google.com", "2222", ["red", "miami", "sun"])

    #renters
    renter1 = Renter("zeinab@google.com", "1234", ["purple", "dearborn", "rola"])
    renter2 = Renter("john@google.com", "abcd", ["blue", "dallas", "joyce"])

    #cars 
    car1 = Car(1, "Toyota Camry", 2020, 30000, "Dearborn", 50, {},  owner1.email)
    car2 = Car(2, "Honda Civic", 2019, 25000, "Detroit", 45, {}, owner1.email)
    car3 = Car(3, "Tesla Model 3", 2021, 15000, "Dearborn Heights", 90, {}, owner2.email)
    car4 = Car(4, "Ford Escape", 2018, 40000, "Ann Arbor", 55, {}, owner2.email)

    #assign cars to owners
    owner1.cars.extend([car1, car2])
    owner2.cars.extend([car3, car4])
    # return everything
    return [owner1, owner2], [renter1, renter2], [car1, car2, car3, car4]

# password recovery (coResponsibility)

def recover_password(user):
    print("\n=== Password Recovery ===")

    # Build chain: q1->q2->q3
    q1 = Question1Handler(user.securityQuestions[0])
    q2 = Question2Handler(user.securityQuestions[1])
    q3 = Question3Handler(user.securityQuestions[2])
    q1.setNext(q2).setNext(q3)

    # ask question 1 and stop chain if wrong 
    ans1 = input("Question 1: What is your favorite color? ")
    if not q1.handle(ans1):
        return

    #ask q2 adn stop if wrong 
    ans2 = input("Question 2: What city were you born in? ")
    if not q2.handle(ans2):
        return

    # ask q3 adn stop chain if wrong 
    ans3 = input("Question 3: What is your mom's name?")
    if not q3.handle(ans3):
        return
    
    #all 3 passed, show it 
    print("Your password is:", user.password)

#register a new user with email,password,and 3 security question answers
def register(users):
    print("\n=== Register ===")
    email = input("Enter email: ").strip()

    # check if email already exists
    for u in users:
        if u.email == email:
            print("An account with this email already exists.")
            return

    password = input("Enter password: ").strip()
    
    # collect answers to the 3 security questions
    print("Set your 3 security questions:")
    q1 = input("Answer to Q1 (What is your favorite color?): ").strip()
    q2 = input("Answer to Q2 (What city were you born in?): ").strip()
    q3 = input("Answer to Q3 (What is your mom's name?): ").strip()
   
    # determine if user is an owner or renter
    print("Are you registering as an (1) Owner or (2) Renter?")
    role = input("Choose 1 or 2: ").strip()

    if role == "1":
        new_user = Owner(email, password, [q1, q2, q3])
    elif role == "2":
        new_user = Renter(email, password, [q1, q2, q3])
    else:
        print("Invalid choice. Registration cancelled.")
        return
    
    # add new user to the shared users list
    users.append(new_user)
    print(f"\nAccount created successfully! You can now log in as {email}.")

# Login System (Singleton)
#only 1 session exists at a time through SessionManager
def login(users):
    session = SessionManager.getInstance()

    while True:
        print("\n=== Login Menu ===")
        print("1. Login")
        print("2. Recover Password")
        print("3. Register")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            email = input("Email: ").strip()
            password = input("Password: ").strip()

            #find user by matchig email and passwrd
            found_user = None
            for user in users:
                if user.email == email and user.password == password:
                    found_user = user
                    break

            if found_user:
                session.currentUser = found_user  # update session without re-authenticating
                print(f"\nWelcome, {email}!")
                return found_user
            else:
                print("Invalid email or password.")

        elif choice == "2":
            email = input("Enter your email: ")
            # find user by email and start recovery process
            for user in users:
                if user.email == email:
                    recover_password(user)
                    break
            else:
                print("User not found.")
        
        elif choice == "3": 
            register(users)

        elif choice == "4":
            print("Goodbye!")
            exit()

        else:
            print("Invalid choice.")

#renter Menu: shows all actions available to a renter
def renter_menu(renter, cars, owners, bookings, chatroom, all_users):
    while True:
        print("\n=== Renter Menu ===")
        print("1. Search Cars")
        print("2. Book a Car")
        print("3. Make Payment")
        print("4. Send Message")
        print("5. View Watchlist")
        print("6. Add Car to Watchlist")
        print("7. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            search_cars(cars)

        elif choice == "2":
            book_car(renter, cars, bookings)

        elif choice == "3":
            make_payment(renter, bookings)

        elif choice == "4":
            send_message(chatroom, renter, all_users)

        elif choice == "5":
            view_watchlist(renter)

        elif choice == "6":
            add_to_watchlist(renter, cars)

        elif choice == "7":
            print("Logging out...")
            return

        else:
            print("Invalid choice.")

#owner menu: show all actions for owner
def owner_menu(owner, cars, bookings, chatroom, all_users):
    while True:
        print("\n=== Owner Menu ===")
        print("1. List a Car")
        print("2. Update Car Price")
        print("3. View Bookings")
        print("4. Send Message")
        print("5. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            owner_list_car(owner, cars)
        elif choice == "2":
            owner_update_price(owner)
        elif choice == "3":
            owner_view_bookings(owner, bookings)
        elif choice == "4":
            send_message(chatroom, owner, all_users)
        elif choice == "5":
            print("Logging out...")
            return
        else:
            print("Invalid choice.")

#owner lists a new car using the builder pattrn
#builder collects car details step by step, director assembles the final object
def owner_list_car(owner, cars):
    print("\n=== List a New Car (Builder Pattern) ===")

    builder = CarListingBuilder()

    #collect user input
    builder.setModel(input("Model: "))
    builder.setYear(int(input("Year: ")))
    builder.setMileage(int(input("Mileage: ")))
    builder.setPickupLocation(input("Pickup Location: "))
    builder.setPricePerDay(float(input("Price per day: ")))

    #director builds  final listing
    director = CarListingDirector()
    listing = director.constructFullListing(builder)

    #convert listing into a Car object
    car_id = len(cars) + 1
    new_car = Car(
        car_id,
        listing.model,
        listing.year,
        listing.mileage,
        listing.pickupLocation,
        listing.pricePerDay,
        {},
        owner.email
    )

    cars.append(new_car)
    owner.cars.append(new_car)

    print(f"Car listed successfully: {new_car.model} (${new_car.pricePerDay}/day)")

# owner updates the price of one of their listed cars
# triggers observer notification to any renters watching the car
def owner_update_price(owner):
    print("\n=== Update Car Price ===")
    if not owner.cars:
        print("You have no listed cars.")
        return

    #show owner their current cars and prices
    for car in owner.cars:
        print(f"{car.carID}. {car.model} - ${car.pricePerDay}/day")

    try:
        car_id = int(input("Enter Car ID to update: "))
        new_price = float(input("Enter new price per day: "))
    except ValueError:
        print("Invalid input.")
        return
    
    # find the car by ID
    car = next((c for c in owner.cars if c.carID == car_id), None)
    if not car:
        print("Car not found.")
        return

    car.updatePrice(new_price)
    print(f"Price updated: {car.model} is now ${car.pricePerDay}/day")

# owner views all bookings made on their cars
def owner_view_bookings(owner, bookings):
    print("\n=== Your Bookings ===")
    owner_bookings = [b for b in bookings if b.car.ownerId == owner.email]
   
    # filter bookings that belong to this owner
    if not owner_bookings:
        print("No bookings for your cars yet.")
        return

    for b in owner_bookings:
        print(f"{b.bookingID}. {b.car.model} from {b.startDate} to {b.endDate} - renter: {b.renter.email} - ${b.totalPrice}")

#show the cars
def show_cars(cars):
    print("\nAvailable Cars:")
    for car in cars:
        print(f"{car.carID}. {car.model} ({car.year}) - ${car.pricePerDay}/day in {car.pickupLocation}")


# Renter: Search cars
def search_cars(cars):
    print("\n=== Search Cars ===")
    keyword = input("Enter model or location keyword (or leave empty to see all): ").lower()
    
    # filter cars by keyword match or return all if empty
    results = []
    for car in cars:
        if keyword in car.model.lower() or keyword in car.pickupLocation.lower() or keyword == "":
            results.append(car)

    if not results:
        print("No cars found.")
    else:
        print("\nSearch Results:")
        for car in results:
            print(f"{car.carID}. {car.model} ({car.year}) - ${car.pricePerDay}/day in {car.pickupLocation}")
    return results

#check if two date ranges overlap
def dates_overlap(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1

#renter: book a car and prevent overlapping
def book_car(renter, cars, bookings):
    print("\n=== Book a Car ===")
    show_cars(cars)

    #select car
    try:
        car_id = int(input("Enter Car ID to book: "))
    except ValueError:
        print("Invalid input.")
        return

    car = next((c for c in cars if c.carID == car_id), None)
    if not car:
        print("Car not found.")
        return

    #enter dates
    try:
        start_year = int(input("Start year (e.g., 2025): "))
        start_month = int(input("Start month (1-12): "))
        start_day = int(input("Start day (1-31): "))
        end_year = int(input("End year: "))
        end_month = int(input("End month: "))
        end_day = int(input("End day: "))
        start_date = date(start_year, start_month, start_day)
        end_date = date(end_year, end_month, end_day)
    except ValueError:
        print("Invalid date.")
        return

    #prevent overlapping bookings
    for b in bookings:
        if b.car.carID == car.carID:
            if dates_overlap(start_date, end_date, b.startDate, b.endDate):
                print("This car is already booked for those dates.")
                return
            
    #create booking
    booking_id = len(bookings) + 1
    booking = Booking(booking_id, car, renter, start_date, end_date)
    bookings.append(booking)

    #update availability calendar
    car.updateAvailability(start_date, end_date)

    print(f"\n Booking created!")
    print(f"Booking ID: {booking.bookingID}")
    print(f"Car: {car.model}")
    print(f"Total Price: ${booking.totalPrice}")


# Renter: Make payment (Proxy)
#PaymentProxy checks authentication before forwarding to real payment service
def make_payment(renter, bookings):
    print("\n=== Make Payment ===")
    if not bookings:
        print("No bookings found.")
        return
    
    #filter bookings that belong to this renter
    print("Your bookings:")
    user_bookings = [b for b in bookings if b.renter == renter]
    if not user_bookings:
        print("You have no bookings.")
        return

    for b in user_bookings:
        print(f"{b.bookingID}. {b.car.model} from {b.startDate} to {b.endDate} - ${b.totalPrice}")

    try:
        bid = int(input("Enter Booking ID to pay for: "))
    except ValueError:
        print("Invalid input.")
        return

    booking = next((b for b in user_bookings if b.bookingID == bid), None)
    if not booking:
        print("Booking not found.")
        return
    #proxy checks authentication then forwards payment to real service
    proxy = PaymentProxy(userAuthenticated=True)
    proxy.processPayment(booking.totalPrice)

    # record the payment object
    payment = Payment(len(user_bookings) + 1, booking, renter, None, booking.totalPrice)
    print(f"Payment recorded. Amount: ${payment.amount}, Status: {payment.status}")

# Messaging (Mediator)
def send_message(chatroom, current_user, all_users):
    print("\n=== Send Message ===")
    print("Users:")
    for idx, u in enumerate(all_users, start=1):
        print(f"{idx}. {u.email}")

    try:
        choice = int(input("Choose a user to message: "))
    except ValueError:
        print("Invalid input.")
        return

    if choice < 1 or choice > len(all_users):
        print("Invalid choice.")
        return

    receiver = all_users[choice - 1]
    # prevent user from messaging themselves
    if receiver.email == current_user.email:
        print("You cannot message yourself.")
        return

    content = input("Enter your message: ")

    sender_chat = ChatUser(current_user.email, current_user.email, chatroom)
    receiver_chat = ChatUser(receiver.email, receiver.email, chatroom)

    sender_chat.send(content)


# Watchlist: Add + View
def add_to_watchlist(renter, cars):
    print("\n=== Add to Watchlist ===")
    show_cars(cars)

    try:
        car_id = int(input("Enter Car ID to watch: "))
        threshold = float(input("Enter price threshold: "))
    except ValueError:
        print("Invalid input.")
        return
    
    # find the car by ID
    car = next((c for c in cars if c.carID == car_id), None)
    if not car:
        print("Car not found.")
        return
    
    #create watchlist entry and attach renter as observer
    watch = WatchList(len(renter.watchlist) + 1, renter, car, threshold)
    renter.watchlist.append(watch)
    watch.addWatch()

# display all cars the renter is currently watching
def view_watchlist(renter):
    print("\n=== Your Watchlist ===")
    if not renter.watchlist:
        print("No cars in watchlist.")
        return

    for w in renter.watchlist:
        print(f"{w.watchID}. {w.car.model} at threshold ${w.priceThreshold}")

# MAIN PROGRAM
if __name__ == "__main__":

    # initialize all data and shared structures
    owners, renters, cars = initialize_data()
    all_users = owners + renters
    bookings = []
    chatroom = DriveShareChat()

    print("\n=== Welcome to DriveShare ===")

    # keep running until user exits
    while True:
        user = login(all_users)
        
        # route to correct menu based on user type
        if isinstance(user, Owner):
            owner_menu(user, cars, bookings, chatroom, all_users)
        else:
            renter_menu(user, cars, owners, bookings, chatroom, all_users)