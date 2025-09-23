#!/usr/bin/env python3

#imports
import server
import json
import maskpass, asyncio, requests 
import sys, os
from time import sleep

#functions
def print_menu():
    clear_screen()
    print("Library Management System Menu")
    print("0. Show Menu")
    print("1. View Books")
    print("2. Add Book")
    print("3. Checkout Book")
    print("4. Return Book")
    if not 'token' in globals():
        print("5. Login")
    else:
        print("5. Logout")
    print("6. Exit")

def hello_world():
    message = server.hello_world()
    print(message["message"])

def login() -> None: # puts token in global scope
    try: # Basic token persistence
        with open('token.txt', 'r') as f:
            global token
            token = f.read().strip()
            if token:
                print("Logged in using saved token.")
                sleep(2)
                return
    except FileNotFoundError:
        pass
    while True:
        email = input("Enter your email: ")
        password = maskpass.askpass("Enter your password: ")
        payload = '{"email": "'+email+'", "password": "'+password+'"}'
        response = requests.post('https://lms.murtsa.dev/auth', data= payload) # TO DO: fix this
        # response = requests.post('http://127.0.0.1:8000/auth', data= payload) # for testing local server
        token = response.text # the request hits the server, but it returns an empty string
        if response.status_code != 200:
            print(f"Login failed. Status code {response.status_code} for reason {response.reason}. \nPlease check your credentials and try again.\n")
            choice = input("Do you want to try again? (y/N): ").lower()
            match choice:
                case 'y':
                    continue
                case 'n' | ''| _:
                    print("Returning to main menu.\n")
                    del token # remove token from global scope
                    return
        elif token == "null" or token == "":
            print("Login failed. Invalid credentials.\n")
            choice = input("Do you want to try again? (y/N): ").lower()
            match choice:
                case 'y':
                    continue
                case 'n' | ''| _:
                    print("Returning to main menu.\n")
                    return
        break
    try: # save token to file
        with open('token.txt', 'w') as f:
            f.write(token)
    except Exception as e:
        print(f"Failed to save token to file: {e}")
    print("Login successful!")
    
    

def get_books():
    response = requests.get('https://lms.murtsa.dev/books')
    # response = requests.get('http://127.0.0.1:8000/books')

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Failed to decode JSON response.\n")
        return []
    if 'error' in data:
        print(f"Error fetching books: {data['error']['message']}\n")
        return []
    books = data['data']
    for book in books:
        print(f"\nTitle: {book['title']}, Author: {book['author']}, ISBN: {book['isbn']}, ID: {book['id']}")

def add_book():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    isbn = input("Enter book ISBN: ")
    headers = {"Authorization": token, "Content-Type": "application/json"}
    payload = {"title": title, "author": author, "isbn": isbn}
    response = requests.put('https://lms.murtsa.dev/book', headers=headers, json=payload)
    # response = requests.put('http://127.0.0.1:8000/book', headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Failed to add book. Status code: {response.status_code}, Response: {response.text}\n")
        return
    print("Book added successfully!\n")
    return
    

def checkout_book():
    get_books()
    book_id = input("Enter the ID of the book you want to checkout: ")
    # TO DO: implement checkout functionality in the backend and call it here
    print(f"Book with ID {book_id} checked out successfully!\n")
    return

def return_book(): # TO DO: implement return functionality in the backend and call it here
    pass

def clear_screen():
    if sys.platform == "win32":
        os.system('cls') # for windows
    else:
        os.system('clear') # for linux, mac, etc.



#main
def main():
    # server.get_db_session()
    try:
        #print("Please Choose an option:")
        print_menu()
        while True:
            number = input("Enter your choice: ")
            match number:
                case "0":
                    print_menu()
                case "1":
                    get_books()
                    
                case "2":
                    if 'token' in globals():
                        add_book()
                    else:
                        print("You must be logged in to add a book.")
                case "3":
                    if 'token' in globals():
                        clear_screen()
                        checkout_book()
                    else:
                        print("You must be logged in to checkout a book.")
                case "4":
                    if 'token' in globals():
                        return_book()
                    else:
                        print("You must be logged in to return a book.")
                case "5":
                    if 'token' in globals():
                        global token # to modify the global token variable
                        del token # remove token from global scope
                        print("Logged out successfully.")
                        print_menu()
                    else:
                        login()
                        print_menu()
                case "6":
                    print("Exiting...")
                    break
                case _:
                    print("Invalid choice. Please try again.")
        
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()