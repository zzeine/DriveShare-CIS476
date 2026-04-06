#subject 

class PaymentService: 
    def processPayment(self, amount): 
        pass

#real subject 
class RealPaymentService (PaymentService): 
    def processPayment(self, amount):
        print(f"Processing real payment of ${amount}...")
        print("Payment successful!")

#proxyy
class PaymentProxy: 
    def __init__(self, userAuthenticated):
        self.userAuthenticated = userAuthenticated    #Store whether the user is authenticated
        self.realService = RealPaymentService()         #proxy holds  reference to real service

    def processPayment(self, amount):
        #security check: only authenticated users can pay
        if not self.userAuthenticated:
            print("Access denied: User not authenticated.")
            return
          #if authenticated forward  request to real service
        print("Proxy: User authenticated. Forwarding request to real payment service...")
        self.realService.processPayment(amount)


