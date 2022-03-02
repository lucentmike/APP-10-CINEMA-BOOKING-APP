from re import search
import sqlite3
import fpdf 


#Create a class for the User that takes in the name, and has a buy method that takes the seat and credit card information 
class User:

    def __init__(self, name):
        self.name = name


    # def buy(self, seat, card):
    #     if user_seat.is_free() == True:
    #         user_seat.occupy() 
            
    #     else:
    #         print("That Seat Is Taken!")


#Create a class for the Seat, that takes in database, seat_id, price. Has a is_free function and occupy fnction to check seat avalibility
class Seat: 

    def __init__(self, seat_id, price=0, database="cinema.db"):
        self.database = database
        self.seat_id = seat_id

        connection = sqlite3.connect("cinema.db")
        cursor = connection.cursor() 
        cursor.execute("""
        SELECT "price" FROM "Seat" WHERE "seat_id" = ?


""", [self.seat_id])

        results = cursor.fetchall()
        connection.close()

        self.price = results[0][0]


    def is_free(self):

        connection = sqlite3.connect("cinema.db")
        cursor = connection.cursor() 
        cursor.execute("""
        SELECT "taken" FROM "Seat" WHERE "seat_id" = ?


""", [self.seat_id])

        results = cursor.fetchall()
        connection.close()

        if int(results[0][0]) == 0:
            return True


    def occupy(self):

        connection = sqlite3.connect("cinema.db")
        connection.execute("""
        UPDATE "Seat" SET "taken"=1 WHERE "seat_id" = ?

    """, [self.seat_id])

        connection.commit()
        connection.close()


#Create a clas for Card that takes in the database, type, number, cvc and holder name. Has a validate function that takes in the price of the seat 

class Card:

    def __init__(self, type, number, cvc, holder, database="banking.db"):
        self. database = database
        self.type = type
        self.number = number 
        self.cvc = cvc
        self.holder = holder


    def validate(self, price):
        pass


#Create a Ticket class that takes in the id, user, price, seat and to_pdf class that prints out a PDF receipt 

class Ticket:

    def __init__(self, id, user, price, seat):
        self.id = id
        self.user = user
        self.price = price
        self.seat = seat

    
    def to_pdf(path):
        pass
    

user = User(name = input("Your Full Name: "))

user_seat = Seat(seat_id = input("Which Seat would you like to purchase?: "))

user_card = Card(type = input("Enter your card Type: "), number = input("Enter your card Number: "), cvc = input("Enter your card CVC: "), holder = input("Enter your card holder Name: "))

#user.buy(seat=user_seat, card=user_card)

print (f'{user_seat.price}')