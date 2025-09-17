#!/usr/bin/env python3

#imports
import server
import json
import maskpass, asyncio
from fastapi import Request

#functions
def print_menu():
    print("1. View Books")
    print("2. Add Book")
    print("3. Checkout Book")
    print("4. Return Book")
    print("5. Login")
    print("6. Exit")

def hello_world():
    message = server.hello_world()
    print(message["message"])

def login():
    email = input("Enter your email: ")
    password = maskpass.askpass("Enter your password: ")
    request = Request(scope= None,send=json.dumps({"email": email, "password": password}).encode('utf-8')) # TO DO: fix this

    #call server auth function
    token = asyncio.run(server.post_auth(request)) # TO DO: pass the correct parameters
    return token
    

def get_books():
    server.get_books()

def add_book():
    server.create_book()

def checkout_book():
    pass

def return_book():
    pass



#main
def main():
    # server.get_db_session()
    hello_world()

    token = login()
    print("Your token is: " + token)

if __name__ == "__main__":
    main()