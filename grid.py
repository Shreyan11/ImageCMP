import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QScrollArea, QTabWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QResizeEvent
import glob
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
import matplotlib.pyplot as plt

# Data for the pie chart
a1 = 0
b1 = 0
g1 = 0

class ImageGrid(QWidget):
    
    def __init__(self, image_paths):
        super().__init__()

        # Create the scroll area and set its widget resizable
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create the grid layout for the images
        grid_layout = QGridLayout()

        # Add the images to the grid
        self.labels = []
        for i, path in enumerate(image_paths):
            # Create the label and set the image
            #print(path)
            label = QLabel(self)
            label.setAlignment(QtCore.Qt.AlignCenter)
            pixmap = QPixmap(path).scaled(100,100,aspectRatioMode=True)
            label.setPixmap(pixmap)
            name_label = QLabel(os.path.basename(path), self)
            name_label.setAlignment(QtCore.Qt.AlignCenter)
            # Add the label to the grid
            self.labels.append((label, name_label))
            grid_layout.addWidget(label, i // 2*2   , i % 2)
            grid_layout.addWidget(name_label, i // 2*2 + 1, i % 2)

        # Set the grid layout as the main layout of the scroll area widget
        widget = QWidget()
        widget.setLayout(grid_layout)
        scroll_area.setWidget(widget)

        # Create the vertical layout for the main widget
        main_layout = QVBoxLayout()

        # Add a button to generate the pie chart
        pie_button = QPushButton('Generate Pie Chart', self)
        pie_button.clicked.connect(self.generate_pie_chart)
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(pie_button)

        # Set the main layout for the widget
        self.setLayout(main_layout)

    def generate_pie_chart(self):
        global a1, b1, g1

        # Calculate the number of good and bad images
        total = a1
        good = g1
        bad = b1

        # Create the pie chart
        labels = ['Good', 'Bad']
        sizes = [good, bad]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')

        # Set the title
        ax.set_title('Image Quality')

        # Show the plot
        plt.show()


class TabWidget(QTabWidget):
    def __init__(self):
        a = os.getcwd()
        g= os.getcwd()
        b = os.getcwd()
        super().__init__()

        # Add the three tabs
        self.tab1 = QWidget()
        self.addTab(self.tab1, "All")

        self.tab2 = QWidget()
        self.addTab(self.tab2, "Good")

        self.tab3 = QWidget()
        self.addTab(self.tab3, "Bad")

        # Set the layout for each tab
        self.tab1_layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1_layout)

        self.tab2_layout = QVBoxLayout()
        self.tab2.setLayout(self.tab2_layout)

        self.tab3_layout = QVBoxLayout()
        self.tab3.setLayout(self.tab3_layout)

        # Add the image grids to each tab
        tab1_images = glob.glob(os.path.join(a, '*.jpg'))
        global a1
        a1 = len(tab1_images)
        tab1_image_grid = ImageGrid(tab1_images)
        
        self.tab1_layout.addWidget(tab1_image_grid)
        
        #print(x)
        tab2_images = glob.glob(os.path.join(g, '*.jpg'))
        
        global g1
        g1 = len(tab2_images)
        tab2_image_grid = ImageGrid(tab2_images)
        self.tab2_layout.addWidget(tab2_image_grid)

        tab3_images = glob.glob(os.path.join(os.path.join(b, '*.jpg')))
        global b1
        b1 = len(tab3_images)
        tab3_image_grid = ImageGrid(tab3_images)
        self.tab3_layout.addWidget(tab3_image_grid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tab_widget = TabWidget()
    tab_widget.show()
    sys.exit(app.exec_())

