import sqlite3
from fpdf import FPDF
import uuid
import webbrowser
import os

#Create a class for the User that takes in the name, and has a buy method that takes the seat and credit card information 
class User:

    def __init__(self, name):
        self.name = name


    def buy(self, seat, card):
        if seat.is_free() == True:
            if card.validate(seat.price) == False:
                 print("There Was An Error With The Card!")
            else:
                print ("Card Accepted, Ticket Purchased!") 
                seat.occupy() 
                user_ticket = Ticket(id = uuid.uuid4().hex[:8], user= self.name, price = seat.price, seat = seat.seat_id)
                user_ticket.to_pdf()
        else:
             print("That Seat Is Taken!")


#Create a class for the Seat, that takes in database, seat_id, price. Has a is_free function and occupy fnction to check seat avalibility
class Seat: 

    def __init__(self, seat_id, price=0, database="cinema.db"):
        self.database = database
        self.seat_id = seat_id

        connection = sqlite3.connect(self.database)
        cursor = connection.cursor() 
        cursor.execute("""
        SELECT "price" FROM "Seat" WHERE "seat_id" = ?


""", [self.seat_id])

        results = cursor.fetchall()
        connection.close()

        self.price = results[0][0]


    def is_free(self):

        connection = sqlite3.connect(self.database)
        cursor = connection.cursor() 
        cursor.execute("""
        SELECT "taken" FROM "Seat" WHERE "seat_id" = ?


""", [self.seat_id])

        results = cursor.fetchall()
        connection.close()

        if int(results[0][0]) == 0:
            return True
        else:
            return False


    def occupy(self):

        connection = sqlite3.connect(self.database)
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
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor() 
        cursor.execute("""
        SELECT "balance" FROM "Card" WHERE "type" = ? AND "number" = ? AND "cvc" = ? AND "holder" = ?


""", [self.type, self.number, self.cvc, self.holder])

        results = cursor.fetchall()
        connection.close()

        if len(results) == 0:
            return False
        else:
            connection = sqlite3.connect(self.database)
            connection.execute("""
            UPDATE "Card" SET "balance"= balance - ? WHERE "type" = ? AND "number" = ? AND "cvc" = ? AND "holder" = ?

        """, [price, self.type, self.number, self.cvc, self.holder])

            connection.commit()
            connection.close()
            return True 
            


#Create a Ticket class that takes in the id, user, price, seat and to_pdf class that prints out a PDF receipt 

class Ticket:

    def __init__(self, id, user, price, seat):
        self.id = id
        self.user = user
        self.price = price
        self.seat = seat

    
    def to_pdf(self):

        filename = str(self.user + "_confirmation")

        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        #Insert Title 
        pdf.set_font(family='Times', size = 24, style='B')
        pdf.cell(w=0, h=80, txt='Your Digital Ticket', border=1, align='C', ln=1)

        #Insert Ticket ID, Name, Price, and Seat
        pdf.set_font(family= "Times", size=14, style ='B')
        pdf.cell(w=100, h=40, txt='Ticket ID:', border=1)
        pdf.cell(w=150, h=40, txt= self.id, border=1, ln=1)

        pdf.cell(w=100, h=25, txt="Name:", border=1)
        pdf.cell(w=150, h=25, txt=self.user, border=1, ln=1)

        pdf.cell(w=100, h=25, txt="Price:", border=1)
        pdf.cell(w=150, h=25, txt=str(self.price), border=1, ln=1)

        pdf.cell(w=100, h=25, txt="Seat ID:", border=1)
        pdf.cell(w=150, h=25, txt=self.seat, border=1, ln=1)


        #Change directory, Print the Pdf
        pdf.output(filename)

        #Open PDF automaticlly, if windows : webbrowser.open(self.filename)
        webbrowser.open('file://'+os.path.realpath(filename))
    

user = User(name = input("Your Full Name: "))

user_seat = Seat(seat_id = input("Which Seat would you like to purchase?: "))

user_card = Card(type = input("Enter your card Type: "), number = input("Enter your card Number: "), cvc = input("Enter your card CVC: "), holder = input("Enter your card holder Name: "))

user.buy(user_seat, user_card)