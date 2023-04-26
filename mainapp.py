from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
import sys
from PyQt6.QtGui import *
from newwin import MyUI
from grid import ImageGrid


class Load(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageCmp 1.0")
        self.setGeometry(100, 200, 300, 200)

        self.progress_bar = QProgressBar()
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.progress_bar)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)

    def start_loading(self):
        # Start the timer and set the maximum value of the progress bar
        self.timer.start(100)

    def update_progress(self):
        # Update the value of the progress bar on each timer event
        if self.progress_bar.value() >= 100:
            # Stop the timer when the progress bar is full
            self.timer.stop()
            # Close the application
            # QApplication.close()
            sys.exit(0)
        else:
            self.progress_bar.setValue(self.progress_bar.value() + 1)


class Actual(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageCmp 1.0")
        self.setGeometry(700, 700, 700, 700)
        # Create the menubar
        menubar = self.menuBar()

        # Create the "Project" menu and add "New" and "Open" options to it
        project_menu = QMenu("Project", self)
        # new_project_action = QAction("New", self)
        # open_project_action = QAction("Open", self)
        # project_menu.addAction(new_project_action)
        # project_menu.addAction(open_project_action)
        new_action = QAction(QIcon("/bug.png"), "&New", self)
        new_action.setStatusTip("Create a new document")
        new_action.setShortcut("Ctrl+N")
        # self.n = MyUI()
        new_action.triggered.connect(self.win)
        project_menu.addAction(new_action)
        menubar.addMenu(project_menu)

        new_action2 = QAction(QIcon("./assets/new.png"), "&Open", self)
        new_action2.setStatusTip("Create a new document")
        new_action2.setShortcut("Ctrl+O")
        # new_action.triggered.connect(self.new_document)
        project_menu.addAction(new_action2)
        menubar.addMenu(project_menu)

        # Create the "Settings" menu and add an option to it
        settings_menu = QMenu("Settings", self)
        # settings_action = QAction("Option", self)
        # settings_menu.addAction(settings_action)
        menubar.addMenu(settings_menu)
        menubar.addSeparator()

    def win(self):
        self.n = MyUI()
        # self.n.create_folder_and_file()
        self.n.setFixedSize(500, 350)
        self.n.show()
        #x=self.n.wind()
        #print(x)

if __name__ == "__main__":
    app = QApplication([])
    a = Actual()

    a.show()
    sys.exit(app.exec())
