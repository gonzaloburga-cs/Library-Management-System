#!/usr/bin/env python3

#imports
import server
import json

#functions
def print_menu():
    print("1. View Books")
    print("2. Add Book")
    print("3. Checkout Book")
    print("4. Return Book")
    print("5. Login")
    print("6. Exit")

def longin():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    #call server auth function
    request = "{\"email\":\""+email+"\"\",\"password\":\""+password+"\"}"
    token = server.post_auth(email, password) # TO DO: pass the correct parameters
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
    server.get_db_session()
    server.hello_world()

if __name__ == "__main__":
    main()