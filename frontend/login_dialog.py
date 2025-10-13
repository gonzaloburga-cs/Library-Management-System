from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QDialog,
    QMessageBox,
)
import requests


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login / Signup")
        self.setFixedSize(300, 150)
        self.setStyleSheet("""background-color: #b29c82;""")

        layout = QVBoxLayout()
        # Username
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Username")
        layout.addWidget(self.email_input)
        self.email_input.setStyleSheet("background-color: white;")
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("background-color: white;")
        layout.addWidget(self.password_input)
        # Login Button
        button_layout = QHBoxLayout()
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        button_layout.addWidget(login_button)
        # Signup Button
        signup_button = QPushButton("Signup")
        signup_button.clicked.connect(self.signup)
        button_layout.addWidget(signup_button)

        # Cancel Button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("styles.css")
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        payload = '{"email": "' + email + '", "password": "' + password + '"}'
        #response = requests.post("https://lms.murtsa.dev/auth", data=payload)
        response = requests.post("http://127.0.0.1:8000/auth", data=payload)
        # for testing local server
        global token
        token = response.text.strip(
            '"'
        )  # the request hits the server, but it returns an empty string
        if response.status_code != 200:
            QMessageBox.warning(
                self,
                "Error",
                f"Login failed. Status code {response.status_code} for reason {response.reason}. \nPlease check your credentials and try again.",
            )
            return

        elif token == "null" or token == "":
            QMessageBox.warning(self, "Error", "Login failed. Invalid credentials.")
            return

        try:  # save token to file
            with open("token.txt", "w") as f:
                f.write(token)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save token to file: {e}")
        QMessageBox.information(self, "Success", "Login successful!")
        self.accept()

    def signup(self):
        email = self.email_input.text()
        password = self.password_input.text()
        payload = '{"email": "' + email + '", "password": "' + password + '"}'
        #response = requests.post("https://lms.murtsa.dev/signup", data=payload)
        response = requests.post("http://127.0.0.1:8000/signup", data=payload)
        # for testing local server

        if response.status_code in [200,201]:
            QMessageBox.information(self, "Success", "Thanks for signing up! You can now log in.")
            return
        else:
            QMessageBox.warning(
                self, "Error", f"Signup failed. Status code {response.status_code} for reason {response.reason}.")
            return

