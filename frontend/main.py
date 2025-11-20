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
    """This Class is the main window. It defines the widgets in the window as well as the layout"""
    def __init__(self):
        self.window_height = 600
        self.window_width = 800
        super(MainWindow, self).__init__()
        self.load_colors()
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, self.window_width, self.window_height)
        #self.setStyleSheet(f"background-color: {self.primary_color};")

        # Create a central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #c9c9c9;")
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header Layout
        self.header = QHBoxLayout()
        self.header.setContentsMargins(10, 10, 10, 10)
        self.header.setSpacing(20)

        # stacked layout
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.setContentsMargins(10, 10, 10, 10)
        self.stacked_layout.setSpacing(20)

        # Add layouts to main
        #main_layout.addLayout(self.header)
        header_widget = QWidget()
        header_widget.setLayout(self.header)
        header_widget.setStyleSheet(f"background-color: {self.primary_color};")

        main_layout.addWidget(header_widget)

        main_layout.addLayout(self.stacked_layout)

        ## Widgets
        # title
        self.header_label = QLabel("Library Management System")
        self.header_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setFixedHeight(50)
        self.header_label.setStyleSheet(f"color: {self.secondary_color};")
        

        # Search box
        self.searchbox = QLineEdit()
        self.searchbox.setPlaceholderText("Search books...")
        self.searchbox.setFixedHeight(30)
        self.searchbox.setFixedWidth(250)
        self.searchbox.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border-radius: 10px;
                padding-left: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #4C721D;
            }
        """)
        self.searchbox.textChanged.connect(self.changed_search)
                        

        # Navigation bar
        self.tabs = QTabWidget()

        # Home Button
        self.home_button = QPushButton("Home")
        self.home_button.setStyleSheet("QPushButton {background-color: #FFFFFF; color: black; } QPushButton:hover {background-color: grey; color: black; }")
        self.home_button.clicked.connect(self.clicked_home)

        # My Books button
        self.books_button = QPushButton("My Books")
        self.books_button.setStyleSheet("QPushButton {background-color: #FFFFFF; color: black; } QPushButton:hover {background-color: grey; color: black; }")
        self.books_button.clicked.connect(self.clicked_books)

        #self.change_button_colors()

        # Login Button
        if self.is_logged_in():
            self.login_button = QPushButton("Logout")
            self.login_button.clicked.connect(self.clicked_logout)
            self.login_button.setStyleSheet("QPushButton {background-color: #FFFFFF; color: black; } QPushButton:hover {background-color: red; color: black; }")
            
        else:
            self.login_button = QPushButton("Login")
            self.login_button.clicked.connect(self.clicked_login)
            self.login_button.setStyleSheet("QPushButton {background-color: #FFFFFF; color: black; } QPushButton:hover {background-color: grey; color: black; }")

        # add widgets to header
        self.header.addWidget(self.header_label)
        self.header.addWidget(self.searchbox)
        self.header.addWidget(self.home_button)
        self.header.addWidget(self.books_button)
        self.header.addWidget(self.login_button)

        # Table of books
        books = self.get_books()
        self.books_table = QTableWidget()
        self.books_table.setRowCount(len(books))
        self.books_table.setColumnCount(4)
        self.books_table.setHorizontalHeaderLabels(["Title", "Author", "ISBN", " "])
        for i, book in enumerate(books):
            self.books_table.setItem(i, 0, QTableWidgetItem(f"{book["title"]}"))
            self.books_table.setItem(i, 1, QTableWidgetItem(f"{book["author"]}"))
            self.books_table.setItem(i, 2, QTableWidgetItem(f"{book["isbn"]}"))
            if book["is_checked_out"] == True:
                self.checkout_button = QPushButton("unavailable")
                self.checkout_button.setEnabled(False)
                self.checkout_button.setStyleSheet("background-color: red; color: white;")
                self.books_table.setCellWidget(i, 3, self.checkout_button)
            else:
                self.checkout_button = QPushButton("Check Out")
                self.checkout_button.setEnabled(True)
                self.checkout_button.setStyleSheet(
                    "QPushButton {background-color: black; color: white;} QPushButton:hover {background-color: #3C3F41; color: white; }"
                )
                self.checkout_button.setProperty("book_id", book["id"])
                self.checkout_button.clicked.connect(self.clicked_checkout)
                self.books_table.setCellWidget(i, 3, self.checkout_button)

        self.books_table.resizeColumnsToContents()
        self.books_table.resizeRowsToContents()
        self.books_table.setSortingEnabled(True)
        self.books_table.verticalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #E0E0E0;
                border: 1px solid black;
            }
        """)
        self.books_table.verticalHeader().setVisible(True)
        self.books_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.books_table.sortByColumn(0, Qt.SortOrder(0))
        header = self.books_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        #Table of books style sheet
        self.books_table.setStyleSheet("""
            QTableWidget {
                background-color: transparent; 
                selection-background-color: #D3D3D3;
                selection-color: black;
                color: black;
                border: none;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #c9c9c9;
                color: black;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)
        #Alternating row colors
        self.books_table.setAlternatingRowColors(True)
        self.books_table.setStyleSheet(self.books_table.styleSheet() + """
            QTableWidget::item:alternate {
                background-color: #FAFAFA;
            }
            QTableWidget::item {
                background-color: #EDEDED;
            }
        """)

        # Checked out books table
        books = self.get_books()
        self.my_books_table = QTableWidget()
        self.my_books_table.setColumnCount(4)
        self.my_books_table.setHorizontalHeaderLabels(
            ["Title", "Author", "Due Date", " "]
        )
        self.my_books_table.resizeColumnsToContents()
        self.my_books_table.resizeRowsToContents()
        self.my_books_table.sortByColumn(0, Qt.SortOrder(0))

        # books_table container to add side padding
        books_table_container = QWidget()
        books_table_layout = QVBoxLayout()
        books_table_layout.setContentsMargins(20, 0, 20, 0)  # left, top, right, bottom
        books_table_layout.addWidget(self.books_table)
        books_table_container.setLayout(books_table_layout)

        # my_books_table container to add side padding
        my_books_table_container = QWidget()
        my_books_table_layout = QVBoxLayout()
        my_books_table_layout.setContentsMargins(20, 0, 20, 0)
        my_books_table_layout.addWidget(self.my_books_table)
        my_books_table_container.setLayout(my_books_table_layout)

 
        # Add widgets to stacked layout
        self.stacked_layout.addWidget(books_table_container)
        self.stacked_layout.addWidget(self.my_books_table)

    # UVU Colors
    def load_colors(self):
        """Load UVU colors from JSON config"""
        default_colors = {"primary": "#4C721D", "secondary": "#FFFFFF"}
        if os.path.exists("colors.json"):
            try:
                with open("colors.json", "r") as f:
                    colors = json.load(f)
                    self.primary_color = colors.get("primary", default_colors["primary"])
                    self.secondary_color = colors.get("secondary", default_colors["secondary"])
            except Exception:
                self.primary_color = default_colors["primary"]
                self.secondary_color = default_colors["secondary"]
        else: 
            self.primary_color = default_colors["primary"]
            self.secondary_color = default_colors["secondary"]


    # methods
    def get_books(self) -> list:
        """This function gets the books from the database and returns the result as a list"""
        response = requests.get("https://lms.murtsa.dev/books")
        # response = requests.get("http://127.0.0.1:8000/books")

        try:
            data = response.json()
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Error", "Failed to decode JSON response.")
            return []
        if "error" in data:
            QMessageBox.warning(
                self, "Error", f"Error fetching books: {data['error']['message']}"
            )
            return []
        books = data["data"]
        if books == []:
            QMessageBox.warning(self, "Error", "There was a connection error")
        return books

    def get_my_books(self) -> list:
        """Gets the books the user has checked out and returns it as a list"""
        if self.is_logged_in() == False:
            return []
        headers = {"Authorization": token, "Content-Type": "application/json"}
        user_id = requests.get("https://lms.murtsa.dev/user", headers=headers)
        # user_id = requests.get("http://127.0.0.1:8000/user", headers=headers)
        user_id = user_id.text.strip('"')
        payload = {"user_id": user_id}
        response = requests.post(
            "https://lms.murtsa.dev/my-books", headers=headers, json=payload
        )
        # response = requests.post(
        #     "http://127.0.0.1:8000/my-books", headers=headers, json=payload
        # )

        if response.status_code == 200:
            try:
                data = response.json()
            except json.JSONDecodeError:
                QMessageBox.warning(self, "Error", "Failed to decode JSON response.")
                return []
            if "error" in data:
                QMessageBox.warning(
                    self, "Error", f"Error fetching books: {data['error']['message']}"
                )
                return []
            try:
                books = data["data"]
            except TypeError:
                QMessageBox.information(self, "Info", data)
                return []
            if books == []:
                QMessageBox.warning(self, "Error", "There was a connection error")
            return books
        else:
            QMessageBox.warning(
                self,
                "Error",
                f"There was an error, code: {response.status_code} {response.text}",
            )
            return []

    def is_logged_in(self) -> bool:
        """Checks to see if the user is logged in, and returns a bool"""
        try:  # Basic token persistence
            with open("token.txt", "r") as f:
                global token
                token = f.read().strip()
                if token:
                    response = requests.get(
                        "https://lms.murtsa.dev/user",
                        headers={"Authorization": token},
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

    def change_button_colors(self) -> None:
        """Updates the colors of the Home and Books buttons"""
        if self.stacked_layout.currentIndex() == 0:
            self.home_button.setStyleSheet("background-color: white; color: black")
            self.books_button.setStyleSheet("color: white")
        elif self.stacked_layout.currentIndex() == 1:
            self.home_button.setStyleSheet("background-color: #b29c82; color: white")
            self.books_button.setStyleSheet("background-color: white; color: black")

    def update_book_list(self):
        """Updates the table of books on the home page"""
        books = self.get_books()
        self.books_table.setSortingEnabled(False)
        for i, book in enumerate(books):
            self.books_table.setItem(i, 0, QTableWidgetItem(f"{book["title"]}"))
            self.books_table.setItem(i, 1, QTableWidgetItem(f"{book["author"]}"))
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
        self.books_table.setSortingEnabled(True)

    def update_my_books_list(self):
        """Updates the table of books on the my books page"""
        books = self.get_my_books()
        self.my_books_table.setSortingEnabled(False)
        self.my_books_table.setRowCount(len(books))
        for i, book in enumerate(books):
            self.my_books_table.setItem(i, 0, QTableWidgetItem(f"{book["title"]}"))
            self.my_books_table.setItem(i, 1, QTableWidgetItem(f"{book["author"]}"))
            self.my_books_table.setItem(i, 2, QTableWidgetItem(f"{book["isbn"]}"))
            self.return_button = QPushButton("Return")
            self.return_button.setStyleSheet("QPushButton {background-color: #FFFFFF; color: black; } QPushButton:hover {background-color: #DDDDDD; color: black; }")
            self.return_button.clicked.connect(self.clicked_return)
            self.my_books_table.setCellWidget(i, 3, self.return_button)
        self.my_books_table.resizeColumnsToContents()
        self.my_books_table.resizeRowsToContents()
        self.my_books_table.setSortingEnabled(True)
        header = self.my_books_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

    # event handlers

    def changed_search(self):
        """Updates the selected item in the tables when text is entered into the search box"""
        text = self.searchbox.toPlainText()
        if text == "":
            self.books_table.setCurrentItem(None)
            self.my_books_table.setCurrentItem(None)

        matching_items1 = self.books_table.findItems(text, Qt.MatchFlag.MatchContains)
        if matching_items1:
            # we have found something
            item = matching_items1[0]  # take the first
            self.books_table.setCurrentItem(item)
        matching_items2 = self.my_books_table.findItems(
            text, Qt.MatchFlag.MatchContains
        )
        if matching_items2:
            item = matching_items2[0]
            self.my_books_table.setCurrentItem(item)

    def clicked_login(self):
        """Spawns the login dialog and updates the login button"""
        if self.is_logged_in():
            QMessageBox.information(self, "Info", "You have been logged in")
            self.login_button.setText("Logout")
            self.login_button.clicked.disconnect()
            self.login_button.clicked.connect(self.clicked_logout)
            return

        self.login_dialog = LoginDialog()
        result = self.login_dialog.exec()
        # if login is successful
        if result == QDialog.DialogCode.Accepted and self.is_logged_in():
            self.login_button.setText("Logout")
            self.login_button.clicked.disconnect()
            self.login_button.clicked.connect(self.clicked_logout)
            return
        #if login fails
        else:
            self.login_button.setText("Login")
            self.login_button.clicked.disconnect()
            self.login_button.clicked.connect(self.clicked_login)
            return


    def clicked_logout(self):
        """Logs out the user and updates the logout button"""
        global token
        requests.post("https://lms.murtsa.dev/logout")
        # response = requests.post("https://lms.murtsa.dev/auth", data=token)
        del token
        self.login_button.setText("Login")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.clicked_login)
        self.clicked_home()
        QMessageBox.information(self, "Info", "You are logged out")

    def clicked_checkout(self):
        """Checks out the desired book"""
        if not self.is_logged_in():
            QMessageBox.warning(
                self, "Error", "You must be logged in to checkout a book"
            )
            return
        headers = {"Authorization": token, "Content-Type": "application/json"}
        sender = self.sender()
        book_id = sender.property("book_id")
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
            QMessageBox.information(self, "Info", response.text.strip('"'))
            self.update_book_list()
        else:
            QMessageBox.warning(
                self, "Error", "Failed to checkout book. {response.text}"
            )
        return

    def clicked_return(self):
        """Returns a book for the logged-in user."""
        headers = {"Authorization": token, "Content-Type": "application/json"}
        sender = self.sender()
        book_id = sender.property("book_id")
        user_id = requests.get("https://lms.murtsa.dev/user", headers=headers)
        # user_id = requests.get('http://127.0.0.1:8000/user', headers=headers)
        if user_id.status_code != 200:
            QMessageBox.warning(
                self, "Error", "Session expired sign in again to return a book"
            )
            return

        payload = {"book_id": book_id, "user_id": user_id.text.strip('"')}
        response = requests.put(
            "https://lms.murtsa.dev/return", headers=headers, json=payload
        )
        # response = requests.put('http://127.0.0.1:8000/return', headers=headers, json=payload)
        if response.status_code == 200:
            QMessageBox.information(self, "Info", response.text.strip('"'))
            self.update_book_list()
            if self.my_books_table.rowCount() > 1:
                self.update_my_books_list()
            else:
                self.my_books_table.setRowCount(0)
                return
        else:
            QMessageBox.warning(
                self,
                "Error",
                f"\nFailed to return book. Status code: {response.status_code}, Response: {response.text}\n",
            )

        return

    def clicked_home(self):
        """Changes the page to the home menu"""
        self.stacked_layout.setCurrentIndex(0)
        #self.change_button_colors()
        self.update_book_list()

    def clicked_books(self):
        """Changes the page to the my books menu"""
        if self.is_logged_in():
            self.stacked_layout.setCurrentIndex(1)
            #self.change_button_colors()
            self.update_my_books_list()
            self.login_button.setText("Logout")
            self.login_button.disconnect()
            self.login_button.clicked.connect(self.clicked_logout)
        else:
            self.clicked_login()
            if self.is_logged_in():
                self.stacked_layout.setCurrentIndex(1)
            #self.change_button_colors()
            self.update_my_books_list()


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
