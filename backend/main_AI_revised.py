#!/usr/bin/env python3

import json
import maskpass
import requests
import os
import sys
import traceback
from time import sleep

SLEEP_TIME = 2  # seconds
API_BASE = "https://lms.murtsa.dev"  # Change to local server for testing if needed


# ------------------------------
# Utility Functions
# ------------------------------

def clear_screen() -> None:
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def api_request(method: str, endpoint: str, token: str = None, **kwargs):
    """
    Wrapper for HTTP requests with error handling.
    Returns (success, response_data_or_text)
    """
    url = f"{API_BASE}{endpoint}"
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = token
    try:
        response = requests.request(method, url, headers=headers, **kwargs)
        try:
            data = response.json()
        except json.JSONDecodeError:
            return False, response.text
        return response.status_code, data
    except requests.RequestException as e:
        return False, str(e)


def headers(token: str = None):
    """Returns headers dictionary with optional authorization token."""
    hdr = {"Content-Type": "application/json"}
    if token:
        hdr["Authorization"] = token
    return hdr


# ------------------------------
# Authentication
# ------------------------------

def is_logged_in() -> str | None:
    """Checks if a saved token exists and is valid. Returns token if logged in."""
    if not os.path.exists("token.txt"):
        return None
    try:
        with open("token.txt", "r") as f:
            token = f.read().strip()
        if not token:
            return None
        status, data = api_request("GET", "/user", token=token)
        if status != 200:
            os.remove("token.txt")
            return None
        print("Logged in using saved token.")
        return token
    except Exception:
        return None


def login() -> str | None:
    """Prompts user for credentials and logs in. Returns token on success."""
    while True:
        email = input("Enter your email: ")
        password = maskpass.askpass("Enter your password: ")
        payload = {"email": email, "password": password}
        status, data = api_request("POST", "/auth", data=json.dumps(payload))
        if status != 200 or data in ("null", ""):
            print("Login failed. Please check your credentials.\n")
            choice = input("Try again? (y/N): ").lower()
            if choice != "y":
                return None
            continue
        token = data.strip('"')
        try:
            with open("token.txt", "w") as f:
                f.write(token)
        except Exception as e:
            print(f"Warning: Failed to save token: {e}")
        print("Login successful!")
        return token


def logout(token: str) -> None:
    """Logs out the user and deletes the saved token."""
    api_request("POST", "/logout", token=token)
    if os.path.exists("token.txt"):
        os.remove("token.txt")
    print("Logged out successfully.")


def signup() -> None:
    """Registers a new user."""
    email = input("Enter your email: ")
    password = maskpass.askpass("Enter your password: ")
    payload = {"email": email, "password": password}
    status, data = api_request("POST", "/signup", data=json.dumps(payload))
    if status in (200, 201):
        print("User created successfully! You can now log in.")
    else:
        print(f"Failed to create user. {data}")
    sleep(SLEEP_TIME)


# ------------------------------
# Library Operations
# ------------------------------

def print_books() -> None:
    """Fetches and prints all books."""
    clear_screen()
    status, data = api_request("GET", "/books")
    if not status or "error" in data:
        print(f"Error fetching books: {data}")
        sleep(SLEEP_TIME)
        return
    books = data.get("data", [])
    print(f"\n{'-'*20} Books {'-'*20}\n")
    for book in books:
        print(
            f"Title: {book['title']}, Author: {book['author']}, "
            f"ISBN: {book['isbn']}, ID: {book['id']}"
        )
    input("\nPress Enter to continue...")


def get_user_id(token: str) -> str | None:
    """Fetches the user ID for a logged-in user."""
    status, data = api_request("GET", "/user", token=token)
    if status != 200:
        print("Session expired. Please log in again.")
        return None
    return data.strip('"')


def print_my_books(token: str) -> None:
    """Displays books checked out by the logged-in user."""
    user_id = get_user_id(token)
    if not user_id:
        return
    payload = {"user_id": user_id}
    status, data = api_request("POST", "/my-books", token=token, json=payload)
    if status != 200 or "error" in data:
        print(f"Error fetching your books: {data}")
        return
    books = data.get("data", [])
    if not books:
        print("No books checked out.")
        return
    print(f"\n{'-'*20} My Books {'-'*20}\n")
    for book in books:
        print(
            f"Title: {book['title']}, Author: {book['author']}, "
            f"ISBN: {book['isbn']}, ID: {book['id']}"
        )


def add_book(token: str) -> None:
    """Adds a new book."""
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    isbn = input("Enter book ISBN: ")
    payload = {"title": title, "author": author, "isbn": isbn}
    status, data = api_request("PUT", "/book", token=token, json=payload)
    if status != 200:
        print(f"Failed to add book: {data}")
        sleep(SLEEP_TIME)
        return
    print("Book added successfully!")
    sleep(SLEEP_TIME)


def checkout_book(token: str) -> None:
    """Checks out a book for the logged-in user."""
    print_books()
    user_id = get_user_id(token)
    if not user_id:
        return
    book_id = input("Enter the ID of the book to checkout: ")
    payload = {"book_id": book_id, "user_id": user_id}
    status, data = api_request("PUT", "/checkout", token=token, json=payload)
    if status == 200:
        print(data.strip('"'))
    else:
        print(f"Failed to checkout book: {data}")
    sleep(SLEEP_TIME)


def return_book(token: str) -> None:
    """Returns a book for the logged-in user."""
    print_my_books(token)
    user_id = get_user_id(token)
    if not user_id:
        return
    book_id = input("Enter the ID of the book to return: ")
    payload = {"book_id": book_id, "user_id": user_id}
    status, data = api_request("PUT", "/return", token=token, json=payload)
    if status == 200:
        print(data.strip('"'))
    else:
        print(f"Failed to return book: {data}")
    sleep(SLEEP_TIME)


# ------------------------------
# Menu
# ------------------------------

def print_menu(token: str = None) -> None:
    """Displays the main menu."""
    clear_screen()
    print("Library Management System Menu")
    print("0. Show Menu")
    print("1. View Books")
    print("2. Add Book")
    print("3. Checkout Book")
    print("4. Return Book")
    if token:
        print("5. Logout")
    else:
        print("5. Login")
        print("7. Sign Up")
    print("6. Exit")


# ------------------------------
# Main
# ------------------------------

def main():
    """Main function to run the CLI library system."""
    token = is_logged_in()

    try:
        while True:
            print_menu(token)
            choice = input("Enter your choice: ")
            match choice:
                case "0":
                    continue
                case "1":
                    print_books()
                case "2":
                    if token:
                        add_book(token)
                    else:
                        print("Login required to add a book.")
                        sleep(SLEEP_TIME)
                case "3":
                    if token:
                        checkout_book(token)
                    else:
                        print("Login required to checkout a book.")
                        sleep(SLEEP_TIME)
                case "4":
                    if token:
                        return_book(token)
                    else:
                        print("Login required to return a book.")
                        sleep(SLEEP_TIME)
                case "5":
                    if token:
                        logout(token)
                        token = None
                    else:
                        token = login()
                    sleep(SLEEP_TIME)
                case "6":
                    print("Exiting...")
                    sleep(SLEEP_TIME)
                    break
                case "7":
                    if not token:
                        signup()
                        sleep(SLEEP_TIME)
                case _:
                    print("Invalid choice. Try again.")
                    sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception:
        traceback.print_exc()
    finally:
        print("Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
