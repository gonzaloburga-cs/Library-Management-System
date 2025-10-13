#!/usr/bin/env python3

# imports
import json
import maskpass, asyncio, requests
import sys, os
import traceback
from time import sleep

sleep_time = 2  # seconds

# functions
def print_menu() -> None:
    """Prints the main menu."""
    clear_screen()
    print("Library Management System Menu")
    print("0. Show Menu")
    print("1. View Books")
    print("2. Add Book")
    print("3. Checkout Book")
    print("4. Return Book")
    if not "token" in globals():
        print("5. Login")
    else:
        print("5. Logout")
    print("6. Exit")
    if not "token" in globals():
        print("7. Sign Up")


def hello_world():
    """Test function to check server connectivity."""
    message = requests.get("https://lms.murtsa.dev/")
    print(message.status_code)

def is_logged_in() -> bool:
    """Check if user is logged in by looking for a saved token."""
    try:  # Basic token persistence
        with open("token.txt", "r") as f:
            global token
            token = f.read().strip()
            if token:
                #response = requests.get("https://lms.murtsa.dev/user", headers={"Authorization": token})
                response = requests.get("http://127.0.0.1:8000/user", headers={"Authorization": token})
                if response.status_code != 200:
                    try:
                        os.remove("token.txt")
                    except Exception:
                        pass
                    del token
                    return False
            print("Logged in using saved token.")
            return True
    except FileNotFoundError:
        return False

def login() -> None:  # puts token in global scope
    """Logs in the user and saves the token to a file."""
    if is_logged_in():
        return
    

    while True:
        email = input("Enter your email: ")
        password = maskpass.askpass("Enter your password: ")
        payload = '{"email": "' + email + '", "password": "' + password + '"}'
        #response = requests.post('https://lms.murtsa.dev/auth', data= payload)
        response = requests.post("http://127.0.0.1:8000/auth", data=payload)
        # for testing local server
        global token
        token = response.text.strip('"')  # the request hits the server, but it returns an empty string
        if response.status_code != 200:
            print(
                f"Login failed. Status code {response.status_code} for reason {response.reason}. \nPlease check your credentials and try again.\n"
            )
            choice = input("Do you want to try again? (y/N): ").lower()
            match choice:
                case "y":
                    continue
                case "n" | "" | _:
                    print("Returning to main menu.\n")
                    del token  # remove token from global scope
                    return
        elif token == "null" or token == "":
            print("Login failed. Invalid credentials.\n")
            choice = input("Do you want to try again? (y/N): ").lower()
            match choice:
                case "y":
                    continue
                case "n" | "" | _:
                    print("Returning to main menu.\n")
                    return
        break
    try:  # save token to file
        with open("token.txt", "w") as f:
            f.write(token)
    except Exception as e:
        print(f"Failed to save token to file: {e}")
    print("Login successful!")

def logout() -> None:
    """Logs out the user and deletes the saved token."""
    global token  # to modify the global token variable
    #requests.post("https://lms.murtsa.dev/logout")
    requests.post("http://127.0.0.1:8000/logout")
    # server.supabase.auth.admin.sign_out(token.strip('"'))
    del token  # remove token from global scope
    return


def signup() -> None:
    """Signs up a new user."""
    email = input("Enter your email: ")
    password = maskpass.askpass("Enter your password: ")
    payload = '{"email": "' + email + '", "password": "' + password + '"}'
    #response = requests.post('https://lms.murtsa.dev/signup', data=payload)
    response = requests.post("http://127.0.0.1:8000/signup", data=payload)
    # for testing local server
    if response.status_code == 200:
        print("User Created Successfully!")
        return
    else:
        print("Failed to create user")
        print_menu()
        return

def print_books() -> None:
    """Fetches and prints the list of books from the server."""
    clear_screen()
    #response = requests.get('https://lms.murtsa.dev/books')
    response = requests.get("http://127.0.0.1:8000/books")

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Failed to decode JSON response.\n")
        sleep(sleep_time)
        return []
    if "error" in data:
        print(f"Error fetching books: {data['error']['message']}\n")
        sleep(sleep_time)
        return []
    books = data["data"]
    print(f"\n{'-'*20} Books {'-'*20}\n")
    for book in books:
        print(
            f"\nTitle: {book['title']}, Author: {book['author']}, ISBN: {book['isbn']}, ID: {book['id']}"
        )
    input("\nPress Enter to continue...")


def add_book() -> None:
    """Adds a new book to the library."""
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    isbn = input("Enter book ISBN: ")
    headers = {"Authorization": token, "Content-Type": "application/json"}
    payload = {"title":title, "author": author, "isbn": isbn }
    #response = requests.put('https://lms.murtsa.dev/book', headers=headers, json=payload)
    response = requests.put("http://127.0.0.1:8000/book", headers=headers, json=payload)
    if response.status_code != 200:
        print(
            f"Failed to add book. Status code: {response.status_code}, Response: {response.text}\n"
        )
        sleep(sleep_time)
        input("Press Enter to continue...")
        return
    print("\nBook added successfully!\n")
    sleep(sleep_time)
    return


def checkout_book() -> None:
    """Checks out a book for the logged-in user."""
    print_books()
    headers = {"Authorization": token, "Content-Type": "application/json"}

    book_id = input("Enter the ID of the book you want to checkout: ")
    #user_id = requests.get("https://lms.murtsa.dev/user", headers=headers)
    user_id = requests.get("http://127.0.0.1:8000/user", headers=headers)

    if user_id.status_code != 200:
        print("Session expired sign in again to checkout a book")
        sleep(sleep_time)
        return

    payload = {"book_id": book_id, "user_id": user_id.text.strip('"')}
    #response = requests.put('https://lms.murtsa.dev/checkout', headers=headers, json=payload)
    response = requests.put('http://127.0.0.1:8000/checkout', headers=headers, json=payload)
    if response.status_code == 200:
        print("\n"+response.text.strip('"'))
        sleep(sleep_time)
    else:
        print(f"\nFailed to checkout book. Status code: {response.status_code}, Response: {response.text}\n")
        sleep(sleep_time)
    return


def return_book() -> None:
    """Returns a book for the logged-in user."""
    print_books()
    headers = {"Authorization": token, "Content-Type": "application/json"}

    book_id = input("Enter the ID of the book you want to return: ")
    #user_id = requests.get("https://lms.murtsa.dev/user", headers=headers)
    user_id = requests.get('http://127.0.0.1:8000/user', headers=headers)
    if user_id.status_code != 200:
        print("Session expired sign in again to return a book")
        return

    payload = {"book_id": book_id, "user_id": user_id.text.strip('"')}
    #response = requests.put('https://lms.murtsa.dev/return', headers=headers, json=payload)
    response = requests.put('http://127.0.0.1:8000/return', headers=headers, json=payload)
    if response.status_code == 200:
        print("\n"+response.text.strip('"'))
        sleep(sleep_time)
    else:
        print(f"\nFailed to return book. Status code: {response.status_code}, Response: {response.text}\n")
        sleep(sleep_time)
    return



def clear_screen() -> None:
    """Clears the terminal screen."""
    if os.name == "nt":
        os.system("cls")  # for windows
    else:
        os.system("clear")  # for linux, mac, etc.




# main
def main():
    """Main function to run the Library Management System."""
    
    if is_logged_in():
        pass
    
    try:
        # print("Please Choose an option:")
        while True:
            print_menu()
            number = input("Enter your choice: ")
            match number:
                case "0":
                    print_menu()
                case "1":
                    print_books()

                case "2":
                    if "token" in globals():
                        add_book()
                    else:
                        print("You must be logged in to add a book.")
                        sleep(sleep_time)
                case "3":
                    if "token" in globals():
                        clear_screen()
                        checkout_book()
                    else:
                        print("You must be logged in to checkout a book.")
                        sleep(sleep_time)
                case "4":
                    if "token" in globals():
                        return_book()
                    else:
                        print("You must be logged in to return a book.")
                        sleep(sleep_time)
                case "5":
                    if "token" in globals():
                        logout()
                        # global token  # to modify the global token variable
                        # del token  # remove token from global scope
                        print("Logged out successfully.")
                        sleep(1)
                        print_menu()
                    else:
                        login()
                        sleep(sleep_time)
                        print_menu()
                case "6":
                    print("Exiting...")
                    sleep(sleep_time)
                    break
                case "7":
                       signup()
                case _:
                    print("Invalid choice. Please try again.")
                    sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        # print(f"An error occurred: {e}")
        traceback.print_exc() # uncomment for debugging
    finally:
        print("Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
