# MATH535 - Final Project - Brandon Cortez - interface.py - 5/3/2024
import sys
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QInputDialog, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap

from logic import embed_message, extract_message

class DigitalForensicsToolkitApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Digital Forensics Toolkit")
        self.setGeometry(100, 100, 800, 600)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a container widget to hold the welcome message label
        welcome_container = QWidget(self)
        welcome_container.setLayout(QVBoxLayout())  # Use a QVBoxLayout for the container widget
        layout.addWidget(welcome_container)

        # Create the welcome message label with styled CSS for background and text
        self.welcome_label = QLabel("Welcome to the Digital Forensics Toolkit!", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet(
            "background-color: #c7dceb; color: black; font-size: 32px; padding: 20px; border-radius: 10px;")

        welcome_container.layout().addWidget(self.welcome_label)  # Add the welcome label to the container widget

        # Create the Begin button to prompt users to take one of two actions
        self.begin_button = QPushButton("Begin", self)
        self.begin_button.clicked.connect(self.choose_operation)
        self.begin_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px;")
        layout.addWidget(self.begin_button)

        # Create the quit button to prompt users if they would like to exit the application
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.quit_application)
        self.quit_button.setStyleSheet("background-color: #F44336; color: white; font-size: 16px;")
        layout.addWidget(self.quit_button)

        # Correctly format the Begin and Quit buttons
        self.begin_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.quit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.loaded_image_path = None
        self.embedded_image_path = None

    def choose_operation(self):
        # Prompt the user to pick one of two features in the application
        operations = ["Embed a Message Into an Image", "Extract a Message From an Image"]
        operation, ok = QInputDialog.getItem(self, "Choose Operation", "Select an operation:", operations, 0, False)
        if ok:
            if operation == "Embed a Message Into an Image":
                self.embed()
            elif operation == "Extract a Message From an Image":
                self.extract()

    def load_image(self):
        # Prompt the user to select an image they wish to load into the app
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.gif)", options=options)
        if filename:
            self.loaded_image_path = filename
            pixmap = QPixmap(filename)
            # Convert to grayscale
            pixmap = pixmap.toImage().convertToFormat(QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(pixmap)
            pixmap = pixmap.scaled(self.welcome_label.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.welcome_label.setPixmap(pixmap)

    def embed(self):
        # Embed a message into the image
        self.load_image()
        if self.loaded_image_path:
            message, ok = QInputDialog.getText(self, "Embed Message", "Enter the message to embed:")
            if ok:
                self.embedded_image = embed_message(self.loaded_image_path, message)
                self.show_info_message("Digital Forensics Toolkit", "'" + message + "' Embedded Successfully")
                save_option = self.prompt_save_option()
                if save_option:
                    self.save_image(self.embedded_image)
                    self.reset_ui()  # Reset UI after saving the embedded image

    def extract(self):
        # Extract a message from an image
        self.load_image()
        if self.loaded_image_path:
            extracted_message = extract_message(self.loaded_image_path)
            if extracted_message == "No embedded message found.":
                self.show_error_message("Extracted Message", extracted_message)
            else:
                self.show_info_message("Extracted Message", extracted_message)
            self.reset_ui()  # Reset UI after displaying the extracted message

    def prompt_save_option(self):
        # Prompt the user if they would like to save their embedded image
        save_option, ok = QInputDialog.getItem(self, "Save Image", "Do you want to save the embedded image?", ["Yes", "No"], 0, False)
        return save_option == "Yes"

    def save_image(self, image):
        # Save a generated image to a specified location
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if filename:
            cv2.imwrite(filename, image)
            self.show_info_message("Digital Forensics Toolkit", "Image saved successfully!")

    def show_welcome_message(self):
        # Set the welcome message
        self.welcome_label.setText("Welcome to the Digital Forensics Toolkit!")
        self.welcome_label.setStyleSheet("background-color: #c7dceb; color: black; font-size: 32px; padding: 20px; border-radius: 10px;")

    def reset_ui(self):
        # Reset UI elements to their initial states
        self.loaded_image_path = None
        self.embedded_image_path = None
        self.show_welcome_message()

    def quit_application(self):
        # Confirm with the user if they would like to exit the application
        reply = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def show_error_message(self, title, message):
        # Show a pop up message with a red 'X' icon
        QMessageBox.critical(self, title, message, QMessageBox.Ok)

    def show_info_message(self, title, message):
        # Show a pop up message with a blue informational icon
        QMessageBox.information(self, title, message, QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DigitalForensicsToolkitApp()
    window.show()
    sys.exit(app.exec_())
