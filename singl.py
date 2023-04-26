from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
import sys
from treshold2 import ImageSimilarity


class ImageViewer(QWidget):
    #isim = ImageSimilarity()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Please select the reference image")

        # Create widgets
        self.image_label = QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.open_button = QPushButton("Open")
        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.next_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Connect signals
        self.open_button.clicked.connect(self.open_image)
        self.next_button.clicked.connect(self.next_image)

        # Initialize variables
        self.image_paths = []
        self.current_image_index = 0

    def open_image(self):
        #options = QFileDialog.
        #options |= QFileDialog.DontUseNativeDialog
        global file_name
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            
            self.image_paths = [file_name]
            self.current_image_index = 0
            self.show_current_image()
            self.next_button.setEnabled(True)
            #return file_name


    
    def next_image(self):
        dir = QFileDialog.getExistingDirectory(self, "Open Folder", "")
        app = QApplication([])
        isim = ImageSimilarity(dir)
        isim.calculate_similarity_scores(file_name)
        #self.show_current_image()
        #return dir

    def show_current_image(self):
        self.next_button.setEnabled(True)

        pixmap = QPixmap(self.image_paths[self.current_image_index])
        thumbnail = pixmap.scaled(300, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(thumbnail)

    # def msgbx()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_viewer = ImageViewer()
    image_viewer.setFixedSize(450,300)

    image_viewer.show()
    #x = image_viewer.open_image()
    #x1 = image_viewer.next_image()
    #isim = ImageSimilarity(x,x1)
    #isim.calculate_similarity_scores(x1)
    sys.exit(app.exec())
