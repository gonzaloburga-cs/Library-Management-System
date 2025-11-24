from __future__ import annotations
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt
import requests
import json
import os


class LoginDialog(QDialog):
    """
    Login and signup dialog for the LMS system.

    Responsibilities:
    - Display username/password inputs
    - Call /auth and /signup API endpoints
    - Save returned auth token
    """

    API_BASE = "https://lms.murtsa.dev"   # change to local for testing

    def __init__(self):
        super().__init__()
        self._load_colors()

        self.setWindowTitle("Login / Signup")
        self.setFixedSize(320, 170)
        self.setStyleSheet(
            f"background-color: {self.primary_color}; color: {self.secondary_color};"
        )

        self._build_ui()

    # -------------------------------------------------------------------------
    # UI CONSTRUCTION
    # -------------------------------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout()

        # Email field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet(self._input_style())
        layout.addWidget(self.email_input)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self._input_style())
        layout.addWidget(self.password_input)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self._styled_button("Login", self.login))
        button_layout.addWidget(self._styled_button("Signup", self.signup))
        button_layout.addWidget(self._styled_button("Cancel", self.reject))

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _styled_button(self, text: str, slot):
        """Create a consistently styled button."""
        btn = QPushButton(text)
        btn.clicked.connect(slot)
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                color: black;
                padding: 6px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #dcdcdc;
            }
            """
        )
        return btn

    def _input_style(self) -> str:
        """Centralized text input style."""
        return """
        QLineEdit {
            background-color: white;
            color: black;
            border: 2px solid transparent;
            border-radius: 10px;
            padding: 7px;
        }
        QLineEdit:focus {
            border: 2px solid #4C721D;
        }
        """

    # -------------------------------------------------------------------------
    # LOGIN & SIGNUP LOGIC
    # -------------------------------------------------------------------------

    def login(self):
        """Send login request and handle token storage."""
        email = self.email_input.text().strip()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter email and password.")
            return

        try:
            response = requests.post(
                f"{self.API_BASE}/auth",
                json={"email": email, "password": password},
                timeout=10,
            )
        except requests.RequestException as e:
            QMessageBox.warning(self, "Network Error", f"Failed to reach server:\n{e}")
            return

        if response.status_code != 200:
            QMessageBox.warning(
                self,
                "Login Failed",
                f"Status {response.status_code}: {response.text}",
            )
            return

        token = response.json()

        if not token or token == "null":
            QMessageBox.warning(self, "Error", "Invalid email or password.")
            return

        self._save_token(token)

        QMessageBox.information(self, "Success", "Login successful!")
        self.accept()

    def signup(self):
        """Send signup request."""
        email = self.email_input.text().strip()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter email and password.")
            return

        try:
            response = requests.post(
                f"{self.API_BASE}/signup",
                json={"email": email, "password": password},
                timeout=10,
            )
        except requests.RequestException as e:
            QMessageBox.warning(self, "Network Error", f"Failed to reach server:\n{e}")
            return

        data = response.json()

        if data.get("status") in (200, 201):
            QMessageBox.information(self, "Success", "Signup complete! Please log in.")
        else:
            QMessageBox.warning(
                self,
                "Signup Failed",
                data.get("message", "Unknown error occurred."),
            )

    # -------------------------------------------------------------------------
    # STORAGE & COLORS
    # -------------------------------------------------------------------------

    def _save_token(self, token: str):
        """Safely save token to a local file."""
        try:
            with open("token.txt", "w") as f:
                f.write(token)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not save token: {e}")

    def _load_colors(self):
        """Load primary/secondary UI colors from config file."""
        default = {"primary": "#4C721D", "secondary": "#FFFFFF"}

        if os.path.exists("colors.json"):
            try:
                with open("colors.json", "r") as file:
                    colors = json.load(file)
                    self.primary_color = colors.get("primary", default["primary"])
                    self.secondary_color = colors.get("secondary", default["secondary"])
                    return
            except Exception:
                pass

        self.primary_color = default["primary"]
        self.secondary_color = default["secondary"]
