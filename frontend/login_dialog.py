from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import requests


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        # Username
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Username")
        layout.addWidget(self.email_input)
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        # Login Button
        button_layout = QHBoxLayout()
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        button_layout.addWidget(login_button)
        # Cancel Button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_credentials(self):
        return self.email_input.text(), self.password_input.text()

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        payload = '{"email": "' + email + '", "password": "' + password + '"}'
        response = requests.post("https://lms.murtsa.dev/auth", data=payload)
        # response = requests.post("http://127.0.0.1:8000/auth", data=payload)
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
        QMessageBox.information(self, "success", "Login successful!")
        self.destroy()

    def clicked_logout(self):
        global token  # to modify the global token variable
        # requests.post("https://lms.murtsa.dev/logout", headers={"Authorization": token})
        del token  # remove token from global scope

        self.login_button.setText("Login")
        self.login_button.clicked.connect(self.clicked_login)
        return
