#!/usr/bin/env python3

# Import necessary modules
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from login_dialog import LoginDialog
import os
import requests
import json


class MainWindow(QMainWindow):
    def __init__(self):
        self.window_height = 600
        self.window_width = 800
        super(MainWindow, self).__init__()
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, self.window_width, self.window_height)

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        self.header = QHBoxLayout()
        self.header.setContentsMargins(10, 10, 10, 10)
        self.header.setSpacing(20)

        # label
        self.header_label = QLabel("Library Management System")
        self.header_label.setFont(QFont("Arial", 24))
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setFixedHeight(50)
        self.header.addWidget(self.header_label)

        # Search box
        self.searchbox = QTextEdit()
        self.searchbox.setPlaceholderText("Search for books...")
        self.searchbox.setGeometry(50, 50, 2, 400)
        self.searchbox.setFixedHeight(30)
        self.searchbox.setFixedWidth(200)
        self.header.addWidget(self.searchbox)
        main_layout.addLayout(self.header)

        # Navigation bar
        self.tabs = QTabWidget()

        self.home_button = QPushButton("Home")
        self.books_button = QPushButton("My Books")
        if self.is_logged_in():
            self.login_button = QPushButton("Logout")
            self.login_button.clicked.connect(self.clicked_logout)
        else:
            self.login_button = QPushButton("Login")
            self.login_button.clicked.connect(self.clicked_login)
        self.header.addWidget(self.home_button)
        self.header.addWidget(self.books_button)
        self.header.addWidget(self.login_button)

        # Book list layout
        book_list_layout = QHBoxLayout()
        book_list_layout.setContentsMargins(10, 10, 10, 10)
        book_list_layout.setSpacing(20)
        main_layout.addLayout(book_list_layout)

        # Add a label
        # label = QLabel("Hello, World!")
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # book_list_layout.addWidget(label)

        # Table of books
        books = self.get_books()
        self.books_table = QTableWidget()
        self.books_table.setRowCount(len(books))
        self.books_table.setColumnCount(4)
        self.books_table.setHorizontalHeaderLabels(["Title", "Author", "ISBN", " "])
        for i, book in enumerate(books):
            self.books_table.setItem(i, 0, QTableWidgetItem(f"Book {book["title"]}"))
            self.books_table.setItem(i, 1, QTableWidgetItem(f"Author {book["author"]}"))
            self.books_table.setItem(i, 2, QTableWidgetItem(f"{book["isbn"]}"))
            if book["is_checked_out"] == True:
                self.checkout_button = QPushButton("unavailable")
                self.checkout_button.setEnabled(False)
                self.checkout_button.setStyleSheet(
                    "background-color: red; color: white;"
                )
                self.books_table.setCellWidget(i, 3, self.checkout_button)
            else:
                self.checkout_button = QPushButton("Check Out")
                self.checkout_button.setEnabled(True)
                self.checkout_button.setStyleSheet(
                    "background-color: black; color: white;"
                )
                self.checkout_button.setProperty("book_id", book["id"])
                self.checkout_button.clicked.connect(self.clicked_checkout)
                self.books_table.setCellWidget(i, 3, self.checkout_button)

        self.books_table.resizeColumnsToContents()
        self.books_table.resizeRowsToContents()

        book_list_layout.addWidget(self.books_table)

    # methods
    def get_books(self) -> list:

        response = requests.get("https://lms.murtsa.dev/books")
        # response = requests.get("http://127.0.0.1:8000/books")

        try:
            data = response.json()
        except json.JSONDecodeError:
            print("Failed to decode JSON response.\n")
            return []
        if "error" in data:
            print(f"Error fetching books: {data['error']['message']}\n")
            return []
        books = data["data"]
        if books == []:
            QMessageBox.warning(self, "Error", "There was a connection error")
        return books

    def is_logged_in(self) -> bool:
        try:  # Basic token persistence
            with open("token.txt", "r") as f:
                global token
                token = f.read().strip()
                if token:
                    response = requests.get(
                        "https://lms.murtsa.dev/user", headers={"Authorization": token}
                    )
                    if response.status_code != 200:
                        try:
                            os.remove("token.txt")
                        except Exception:
                            pass
                        del token
                        return False
                else:
                    return False
                print("Logged in using saved token.")
                return True
        except FileNotFoundError:
            return False

    # click events

    def clicked_login(self):
        if self.is_logged_in():
            QMessageBox.information(self, "Info", "You are already logged in")
            self.login_button.setText("Logout")
            self.login_button.clicked.connect()
            return

        self.login_dialog = LoginDialog()
        return

    def clicked_logout(self):
        global token
        # response = requests.post("https://lms.murtsa.dev/auth", data=token)
        del token
        QMessageBox.information(self, "Error", "You are logged out")

    def clicked_checkout(self):  # Untested code from cli
        if not self.is_logged_in():
            QMessageBox.warning(
                self, "Error", "You must be logged in to checkout a book"
            )
            return
        headers = {"Authorization": token, "Content-Type": "application/json"}

        book_id = QObject.sender()["book_id"]
        user_id = requests.get("https://lms.murtsa.dev/user", headers=headers)
        # user_id = requests.get("http://127.0.0.1:8000/user", headers=headers)

        if user_id.status_code != 200:
            QMessageBox.warning(
                self, "Error", "Session expired sign in again to checkout a book"
            )
            return

        payload = {"book_id": book_id, "user_id": user_id.text.strip('"')}
        response = requests.put(
            "https://lms.murtsa.dev/checkout", headers=headers, json=payload
        )
        # response = requests.put('http://127.0.0.1:8000/checkout', headers=headers, json=payload)
        if response.status_code == 200:
            QMessageBox.information(self, response.text.strip('"'))
        else:
            QMessageBox.warning(
                self, "Error", "Failed to checkout book. {response.text}"
            )
        return


def main():
    app = QApplication([])

    # Create main window
    main_window = MainWindow()

    # Show the main window
    main_window.show()

    # Run the application event loop
    app.exec()


if __name__ == "__main__":
    main()
