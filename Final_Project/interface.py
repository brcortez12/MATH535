import sys
from PyQt5.QtWidgets import QApplication, QInputDialog, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap

from logic import embed_message, extract_message, display_LSBs

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

        self.load_button = QPushButton(QIcon("icons/open.png"), "Load Image", self)
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        self.embed_button = QPushButton(QIcon("icons/embed.png"), "Embed Message", self)
        self.embed_button.clicked.connect(self.embed_message)
        layout.addWidget(self.embed_button)

        self.extract_button = QPushButton(QIcon("icons/extract.png"), "Extract Message", self)
        self.extract_button.clicked.connect(self.extract_message)
        layout.addWidget(self.extract_button)

        self.lsb_button = QPushButton(QIcon("icons/lsb.png"), "View Changed LSBs", self)
        self.lsb_button.clicked.connect(self.display_LSBs)
        layout.addWidget(self.lsb_button)

        self.quit_button = QPushButton(QIcon("icons/quit.png"), "Quit", self)
        self.quit_button.clicked.connect(self.quit_application)
        layout.addWidget(self.quit_button)

        self.loaded_image = None

    def load_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.gif)", options=options)
        if filename:
            pixmap = QPixmap(filename)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.loaded_image = filename

    def embed_message(self):
        if self.loaded_image:
            message, ok = QInputDialog.getText(self, "Embed Message", "Enter the message to embed:")
            if ok:
                embed_message(self.loaded_image, message)
        else:
            self.show_error_message("Error", "No image loaded!")

    def extract_message(self):
        if self.loaded_image:
            extracted_message = extract_message(self.loaded_image)
            self.show_info_message("Extracted Message", extracted_message)
        else:
            self.show_error_message("Error", "No image loaded!")

    def display_LSBs(self):
        if self.loaded_image:
            display_LSBs(self.loaded_image)
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
