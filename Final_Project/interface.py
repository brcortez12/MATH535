import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog

class ImageLoaderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Loader")
        self.setGeometry(100, 100, 400, 200)

        # Create a central widget and set a layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a label to display the loaded image
        self.image_label = QLabel("No image loaded", self)
        layout.addWidget(self.image_label)

        # Create a button for loading an image
        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

    def load_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.gif)", options=options)
        if filename:
            self.image_label.setText(f"Image loaded: {filename}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageLoaderApp()
    window.show()
    sys.exit(app.exec_())
