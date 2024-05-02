# MATH535 - Final Project - Brandon Cortez
import sys
from skimage import io, util, color
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QInputDialog, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QImage, QPixmap

from logic import embed_message, extract_message, difference_LSBs

class DigitalForensicsToolkitApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Digital Forensics Toolkit")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.image_label = QLabel("No image loaded", self)
        layout.addWidget(self.image_label)

        self.display_label = QLabel("No image generated", self)
        layout.addWidget(self.display_label)

        self.load_button = QPushButton(QIcon("icons/open.png"), "Load Image", self)
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        self.embed_button = QPushButton(QIcon("icons/embed.png"), "Embed Message", self)
        self.embed_button.clicked.connect(self.embed)
        layout.addWidget(self.embed_button)

        self.extract_button = QPushButton(QIcon("icons/extract.png"), "Extract Message", self)
        self.extract_button.clicked.connect(self.extract)
        layout.addWidget(self.extract_button)

        self.lsb_button = QPushButton(QIcon("icons/lsb.png"), "View Changed LSBs", self)
        self.lsb_button.clicked.connect(self.display_LSBs)
        layout.addWidget(self.lsb_button)

        self.quit_button = QPushButton(QIcon("icons/quit.png"), "Quit", self)
        self.quit_button.clicked.connect(self.quit_application)
        layout.addWidget(self.quit_button)

        self.loaded_image_path = None
        self.embedded_image_path = None
        self.difference_image_path = None

    def load_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.gif)", options=options)
        if filename:
            self.loaded_image_path = filename
            cover_image = io.imread(filename)
            cover_image_gray = color.rgb2gray(cover_image)
            self.loaded_image = util.img_as_ubyte(cover_image_gray)
            
            pixmap = QPixmap(filename)
            # Convert to grayscale
            pixmap = pixmap.toImage().convertToFormat(QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(pixmap)
            pixmap = pixmap.scaled(self.image_label.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

    def embed(self):
        if self.loaded_image_path:
            message, ok = QInputDialog.getText(self, "Embed Message", "Enter the message to embed:")
            if ok:
                self.embedded_image, self.embedded_image_path = embed_message(self.loaded_image_path, message)
                self.show_info_message("Digital Forensics Toolkit", "'" + message + "' Embedded Successfully")
        else:
            self.show_error_message("Error", "No image loaded!")

    def extract(self):
        if self.embedded_image_path is not None:
            extracted_message = extract_message(self.embedded_image)
            self.show_info_message("Extracted Message", extracted_message)
        else:
            self.show_error_message("Error", "No embedded image loaded!")

    def display_LSBs(self):
        if self.embedded_image_path is not None:
            self.difference_image_path = difference_LSBs(self.loaded_image, self.embedded_image)
            if self.difference_image_path:
                pixmap = QPixmap(self.difference_image_path)
                # Convert to grayscale
                pixmap = pixmap.toImage().convertToFormat(QImage.Format_Grayscale8)
                pixmap = QPixmap.fromImage(pixmap)
                pixmap = pixmap.scaled(self.display_label.size(), aspectRatioMode=Qt.KeepAspectRatio)
                self.display_label.setPixmap(pixmap)
        else:
            self.show_error_message("Error", "No image loaded!")

    def quit_application(self):
        QApplication.quit()

    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message, QMessageBox.Ok)

    def show_info_message(self, title, message):
        QMessageBox.information(self, title, message, QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DigitalForensicsToolkitApp()
    window.show()
    sys.exit(app.exec_())
