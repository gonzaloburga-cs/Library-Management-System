from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import Qt

class BaseModal(QDialog):
    def __init__(self, title: str, content_widget: QWidget):
        super().__init__()
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(400, 300)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(content_widget)
        self.setLayout(layout)

        # Styling 
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 8px;
            }
        """)

# Test
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QLabel
    import sys

    app = QApplication(sys.argv)
    test_modal = BaseModal("Test Modal", QLabel("This is a test modal"))
    test_modal.exec()

