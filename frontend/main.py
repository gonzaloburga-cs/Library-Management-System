#!/usr/bin/env python3

# Import necessary modules
import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtCore as QtCore
import PyQt6.QtGui as QtGui

# Fuctions

# click events


def main():
    app = QtWidgets.QApplication([])

    # Create main window
    main_window = QtWidgets.QMainWindow()
    main_window.setWindowTitle("Library Management System")
    main_window.setGeometry(100, 100, 800, 600)

    # Create a central widget
    central_widget = QtWidgets.QWidget()
    main_window.setCentralWidget(central_widget)

    # Create a layout
    layout = QtWidgets.QBoxLayout()
    central_widget.setLayout(layout)

    # Add a label
    label = QtWidgets.QLabel("Hello, World!")
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label)

    # Add a button
    button = QtWidgets.QPushButton("Click Me")
    layout.addWidget(button)

    # Show the main window
    main_window.show()

    # Run the application event loop
    app.exec()


if __name__ == "__main__":
    main()
