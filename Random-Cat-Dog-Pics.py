import random
import sys
import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
import requests
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Click me for new cat image",self)
        self.button2 = QPushButton("Click me for new Dog image",self)
        self.button2.setObjectName("button2")
        self.button.setObjectName("button")
        self.button.clicked.connect(self.cat_api)
        self.button2.clicked.connect(self.dog_api)
        self.image_label = QLabel("no cat loaded",self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button3 = QPushButton("Mort's cat",self)
        self.button3.setObjectName("button3")
        self.button3.clicked.connect(self.special_cats)
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Cat API")
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(self.button3)
        vbox.addWidget(self.button)
        vbox.addWidget(self.button2)
        self.setLayout(vbox)
        self.setStyleSheet("""
        QPushButton {color: black;
        border: 1px solid black;
        border-radius: 10px;
        font-size: 45px;
        }
        QPushButton#button:hover {
        background-color:grey;
        }
        QPushButton#button2:hover {background-color:grey;}
        QPushButton#button3:hover {background-color:grey;}
        """)

    def cat_api(self):
        cat_url = "https://api.thecatapi.com/v1/images/search"
        request = requests.get(cat_url)
        data = request.json()
        cat_image = data[0]["url"]
        image_data = requests.get(cat_image).content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        scaled_pixmap = pixmap.scaledToWidth(400)
        self.image_label.setPixmap(scaled_pixmap)
    def dog_api(self):
        dog_url = "https://dog.ceo/api/breeds/image/random"
        request = requests.get(dog_url)
        data = request.json()
        dog_image = data["message"]
        image_data = requests.get(dog_image).content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        scaled_pixmap = pixmap.scaled(
            400, 400,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
    def special_cats(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_folder = os.path.join(base_dir, "images")
        if os.path.exists(image_folder) and os.listdir(image_folder):
            all_images = os.listdir(image_folder)
            random_image = random.choice(all_images)
            full_path = os.path.join(image_folder, random_image)
            pixmap = QPixmap(full_path)
            scaled_pixmap = pixmap.scaled(400, 400,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText("No images found")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
