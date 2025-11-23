#!/usr/bin/env python3
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from login_dialog import LoginDialog
from datetime import datetime, timedelta
import os
import requests
import json

class MainWindow(QMainWindow):
    """Main Window for the Library Management System GUI."""

    def __init__(self):
        super().__init__()
        self.window_width = 800
        self.window_height = 600

        # Load colors from config
        self.load_colors()

        # Window setup
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, self.window_width, self.window_height)

        # Central widget
        central_widget = QWidget()
        central_widget.setStyleSheet(f"background-color: #c9c9c9;")
        self.setCentralWidget(central_widget)

        # Layouts
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(10, 10, 10, 10)
        self.header_layout.setSpacing(20)

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.setContentsMargins(10, 10, 10, 10)
        self.stacked_layout.setSpacing(20)

        # Add header and stacked layout to main layout
        header_widget = QWidget()
        header_widget.setLayout(self.header_layout)
        header_widget.setStyleSheet(f"background-color: {self.primary_color};")
        self.main_layout.addWidget(header_widget)
        self.main_layout.addLayout(self.stacked_layout)

        # Initialize widgets
        self.setup_header_widgets()
        self.setup_books_table()
        self.setup_my_books_table()
        self.populate_books_table()
        self.populate_my_books_table()

    # ------------------------------
    # UI Setup Methods
    # ------------------------------

    def load_colors(self):
        """Load primary and secondary colors from JSON or use defaults."""
        default_colors = {"primary": "#4C721D", "secondary": "#FFFFFF"}
        try:
            if os.path.exists("colors.json"):
                with open("colors.json", "r") as f:
                    colors = json.load(f)
                    self.primary_color = colors.get("primary", default_colors["primary"])
                    self.secondary_color = colors.get("secondary", default_colors["secondary"])
            else:
                self.primary_color = default_colors["primary"]
                self.secondary_color = default_colors["secondary"]
        except Exception:
            self.primary_color = default_colors["primary"]
            self.secondary_color = default_colors["secondary"]

    def setup_header_widgets(self):
        """Set up the header widgets: title, search box, and buttons."""
        # Title
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
        self.searchbox.setStyleSheet(
            """
            QLineEdit {
                background-color: white;
                color: black;
                border-radius: 10px;
                padding-left: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #4C721D;
            }
            """
        )
        self.searchbox.textChanged.connect(self.changed_search)

        # Home Button
        self.home_button = QPushButton("Home")
        self.home_button.setStyleSheet(
            "QPushButton {background-color: #FFFFFF; color: black; } "
            "QPushButton:hover {background-color: grey; color: black; }"
        )
        self.home_button.clicked.connect(self.clicked_home)

        # My Books Button
        self.books_button = QPushButton("My Books")
        self.books_button.setStyleSheet(
            "QPushButton {background-color: #FFFFFF; color: black; } "
            "QPushButton:hover {background-color: grey; color: black; }"
        )
        self.books_button.clicked.connect(self.clicked_books)

        # Login / Logout Button
        if self.is_logged_in():
            self.login_button = QPushButton("Logout")
            self.login_button.clicked.connect(self.clicked_logout)
            self.login_button.setStyleSheet(
                "QPushButton {background-color: #FFFFFF; color: black; } "
                "QPushButton:hover {background-color: red; color: black; }"
            )
        else:
            self.login_button = QPushButton("Login")
            self.login_button.clicked.connect(self.clicked_login)
            self.login_button.setStyleSheet(
                "QPushButton {background-color: #FFFFFF; color: black; } "
                "QPushButton:hover {background-color: grey; color: black; }"
            )

        # Add header widgets
        self.header_layout.addWidget(self.header_label)
        self.header_layout.addWidget(self.searchbox)
        self.header_layout.addWidget(self.home_button)
        self.header_layout.addWidget(self.books_button)
        self.header_layout.addWidget(self.login_button)

    def setup_books_table(self):
        """Sets up the main books table with styles and headers."""
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(4)
        self.books_table.setHorizontalHeaderLabels(["Title", "Author", "ISBN", " "])
        self.books_table.setSortingEnabled(True)
        self.books_table.setAlternatingRowColors(True)
        self.books_table.setStyleSheet(
            """
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
            QTableWidget::item:alternate {
                background-color: #FAFAFA;
            }
            QTableWidget::item {
                background-color: #EDEDED;
            }
            """
        )
        header = self.books_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        # Container with padding
        books_table_container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 0, 20, 0)
        layout.addWidget(self.books_table)
        books_table_container.setLayout(layout)
        self.stacked_layout.addWidget(books_table_container)

    def setup_my_books_table(self):
        """Sets up the user's checked-out books table."""
        self.my_books_table = QTableWidget()
        self.my_books_table.setColumnCount(4)
        self.my_books_table.setHorizontalHeaderLabels(["Title", "Author", "Due Date", " "])
        header = self.my_books_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        # Container with padding
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 0, 20, 0)
        layout.addWidget(self.my_books_table)
        container.setLayout(layout)
        self.stacked_layout.addWidget(container)

    # ------------------------------
    # Backend Methods
    # ------------------------------

    def get_books(self) -> list:
        """Fetch all books from the API."""
        try:
            response = requests.get("https://lms.murtsa.dev/books")
            response.raise_for_status()
            data = response.json()
            if "data" not in data:
                QMessageBox.warning(self, "Error", "No book data received.")
                return []
            return data["data"]
        except requests.RequestException as e:
            QMessageBox.warning(self, "Error", f"Failed to fetch books: {str(e)}")
            return []

    def get_my_books(self) -> list:
        """Fetch books checked out by the logged-in user."""
        if not self.is_logged_in():
            return []
        headers = {"Authorization": token, "Content-Type": "application/json"}
        try:
            user_id = requests.get("https://lms.murtsa.dev/user", headers=headers).text.strip('"')
            payload = {"user_id": user_id}
            response = requests.post("https://lms.murtsa.dev/my-books", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except requests.RequestException as e:
            QMessageBox.warning(self, "Error", f"Failed to fetch your books: {str(e)}")
            return []

    def is_logged_in(self) -> bool:
        """Check if user is logged in by reading token.txt and verifying session."""
        global token
        try:
            with open("token.txt", "r") as f:
                token = f.read().strip()
                if not token:
                    return False
                resp = requests.get("https://lms.murtsa.dev/user", headers={"Authorization": token})
                if resp.status_code != 200:
                    os.remove("token.txt")
                    del token
                    return False
            return True
        except FileNotFoundError:
            return False

    # ------------------------------
    # Table Update Methods
    # ------------------------------

    def populate_books_table(self):
        """Fill the books table with book data."""
        books = self.get_books()
        self.books_table.setRowCount(len(books))
        for i, book in enumerate(books):
            self.books_table.setItem(i, 0, QTableWidgetItem(book["title"]))
            self.books_table.setItem(i, 1, QTableWidgetItem(book["author"]))
            self.books_table.setItem(i, 2, QTableWidgetItem(book["isbn"]))

            btn = QPushButton("Check Out")
            if book.get("is_checked_out", False):
                btn.setText("Unavailable")
                btn.setEnabled(False)
                btn.setStyleSheet("background-color: red; color: white;")
            else:
                btn.setEnabled(True)
                btn.setStyleSheet("background-color: black; color: white;")
                btn.setProperty("book_id", book["id"])
                btn.clicked.connect(self.clicked_checkout)
            self.books_table.setCellWidget(i, 3, btn)
        self.books_table.resizeColumnsToContents()
        self.books_table.resizeRowsToContents()

    def populate_my_books_table(self):
        """Fill the my_books table with user-specific checked-out books."""
        books = self.get_my_books()
        self.my_books_table.setRowCount(len(books))
        current_date = datetime.now()
        fourteen_days_ago = current_date - timedelta(days=14)

        for i, book in enumerate(books):
            due_date_str = book.get("due_date", "N/A")
            self.my_books_table.setItem(i, 0, QTableWidgetItem(book["title"]))
            self.my_books_table.setItem(i, 1, QTableWidgetItem(book["author"]))
            self.my_books_table.setItem(i, 2, QTableWidgetItem(due_date_str))

            btn = QPushButton("Return")
            if due_date_str != "N/A":
                due_date_obj = datetime.strptime(due_date_str, "%Y-%m-%d")
                if due_date_obj < fourteen_days_ago:
                    btn.setText("Return (Late)")
            btn.setProperty("book_id", book["id"])
            btn.setStyleSheet(
                "QPushButton {background-color: #FFFFFF; color: black; } QPushButton:hover {background-color: #DDDDDD; color: black; }"
            )
            btn.clicked.connect(self.clicked_return)
            self.my_books_table.setCellWidget(i, 3, btn)

        self.my_books_table.resizeColumnsToContents()
        self.my_books_table.resizeRowsToContents()

    # ------------------------------
    # Event Handlers
    # ------------------------------

    def changed_search(self):
        """Highlight matching items in tables based on search text."""
        text = self.searchbox.text()
        if not text:
            self.books_table.setCurrentItem(None)
            self.my_books_table.setCurrentItem(None)
            return

        for table in [self.books_table, self.my_books_table]:
            matches = table.findItems(text, Qt.MatchFlag.MatchContains)
            if matches:
                table.setCurrentItem(matches[0])

    def clicked_login(self):
        """Handle login dialog and button state."""
        if self.is_logged_in():
            QMessageBox.information(self, "Info", "Already logged in")
            self.login_button.setText("Logout")
            self.login_button.clicked.disconnect()
            self.login_button.clicked.connect(self.clicked_logout)
            return

        dialog = LoginDialog()
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted and self.is_logged_in():
            self.login_button.setText("Logout")
            self.login_button.clicked.disconnect()
            self.login_button.clicked.connect(self.clicked_logout)
        else:
            self.login_button.setText("Login")
            self.login_button.clicked.disconnect()
            self.login_button.clicked.connect(self.clicked_login)

    def clicked_logout(self):
        """Logs out user and updates button."""
        global token
        try:
            requests.post("https://lms.murtsa.dev/logout")
        except requests.RequestException:
            pass
        del token
        self.login_button.setText("Login")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.clicked_login)
        self.clicked_home()
        QMessageBox.information(self, "Info", "Logged out successfully")

    def clicked_checkout(self):
        """Checks out a book for the logged-in user."""
        if not self.is_logged_in():
            QMessageBox.warning(self, "Error", "You must log in to checkout a book")
            return

        sender = self.sender()
        book_id = sender.property("book_id")
        headers = {"Authorization": token, "Content-Type": "application/json"}

        user_resp = requests.get("https://lms.murtsa.dev/user", headers=headers)
        if user_resp.status_code != 200:
            QMessageBox.warning(self, "Error", "Session expired, please log in again")
            return

        payload = {"book_id": book_id, "user_id": user_resp.text.strip('"')}
        try:
            response = requests.put("https://lms.murtsa.dev/checkout", headers=headers, json=payload)
            response.raise_for_status()
            QMessageBox.information(self, "Info", response.text.strip('"'))
            self.populate_books_table()
        except requests.RequestException as e:
            QMessageBox.warning(self, "Error", f"Failed to checkout book: {str(e)}")

    def clicked_return(self):
        """Returns a book for the logged-in user."""
        sender = self.sender()
        book_id = sender.property("book_id")
        if not book_id:
            QMessageBox.warning(self, "Error", "Cannot determine book to return")
            return

        headers = {"Authorization": token, "Content-Type": "application/json"}
        user_resp = requests.get("https://lms.murtsa.dev/user", headers=headers)
        if user_resp.status_code != 200:
            QMessageBox.warning(self, "Error", "Session expired, please log in again")
            return

        payload = {"book_id": book_id, "user_id": user_resp.text.strip('"')}
        try:
            response = requests.put("https://lms.murtsa.dev/return", headers=headers, json=payload)
            response.raise_for_status()
            QMessageBox.information(self, "Info", response.text.strip('"'))
            self.populate_books_table()
            self.populate_my_books_table()
        except requests.RequestException as e:
            QMessageBox.warning(self, "Error", f"Failed to return book: {str(e)}")

    def clicked_home(self):
        """Switch to home page."""
        self.stacked_layout.setCurrentIndex(0)
        self.populate_books_table()

    def clicked_books(self):
        """Switch to my books page."""
        if self.is_logged_in():
            self.stacked_layout.setCurrentIndex(1)
            self.populate_my_books_table()
        else:
            self.clicked_login()
            if self.is_logged_in():
                self.stacked_layout.setCurrentIndex(1)
                self.populate_my_books_table()


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
