# MUST INSTALL requests IN YOUR VIRTUAL ENVIRONMENT
import sys
import requests
# not sure why my editor is giving me errors for the imports below
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap

img_url = 'https://halu-test-bucket.s3.amazonaws.com/image-data/Abactochromis_labrosus_0003.jpg'

app = QApplication([])

img = QImage()
img.loadFromData(requests.get(img_url).content)

img_label = QLabel()
img_label.setPixmap(QPixmap(img))
img_label.show()

app.exec_()