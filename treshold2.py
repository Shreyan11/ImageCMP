from skimage.metrics import structural_similarity
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5 import QtWidgets, QtGui, QtCore
from pymongo import *
import pymongo
import os
import shutil
from grid import TabWidget
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

# app = QApplication([])
# msgBox = QMessageBox()
# msgBox.setText("Please wait...")
# msgBox.exec_()


# from singl import ImageViewer
class ImageSimilarity:
    def __init__(self, after_dir):
        global flag
        flag = 0
        global al, gd, bd
        self.after_dir = after_dir

        # connect to MongoDB and select database

        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client["ImageCP"]
        coll = db["table"]
        last_added_doc = coll.find_one(sort=[("_id", pymongo.DESCENDING)])
        global sku
        file1 = last_added_doc["table"]
        sku = last_added_doc["sku"]
        self.coll2 = db[file1]
        print(file1)
        self.folder_path = os.path.join(os.getcwd(), file1)
        os.makedirs(self.folder_path)
        # #self.folder_path = os.path.join(os.getcwd(), ref)
        os.makedirs(os.path.join(self.folder_path, "good"))
        os.makedirs(os.path.join(self.folder_path, "bad"))
        os.makedirs(os.path.join(self.folder_path, "all"))

        # dir = os.makedirs(os.path.join(folder_path, "good"))
        # print("yeet")
        # os.chdir(folder_path)
        # max_mtime = 0
        # max_collection = None
        # for collection in collections:
        #     if 'updated_at' in db[collection].find_one():
        #         mtime = db[collection].find_one(sort=[('updated_at', pymongo.DESCENDING)])['updated_at']
        #         if mtime > max_mtime:
        #             max_mtime = mtime
        #             max_collection = collection

        #             print(max_collection)
        #     else:
        #         print("none")

        # self.folder_path = os.getcwd()

    # print(last_name)
    def calculate_similarity_scores(self, before_image_path):
        # msgBox = QMessageBox()
        # msgBox.setText("Please wait...")
        # msgBox.exec_()
        # Load the "before" image
        before = cv2.imread(before_image_path)
        #app = QApplication([])

        # Loop through all JPG files in the selected directory and calculate the similarity score for each
        for entry in os.scandir(self.after_dir):
            if entry.is_file() and entry.name.endswith(".jpg"):
                # s the "after" image
                after = cv2.imread(entry.path)

                # Convert images to grayscale
                before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
                after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

                # Compute SSIM between two images
                (score, diff) = structural_similarity(
                    before_gray, after_gray, full=True, data_range=255
                )
                # print(score)
                src_path = entry.path
                dst_path = os.path.join(self.folder_path, "all", entry.name)
                al = dst_path
                shutil.copyfile(src_path, dst_path)
                if score == 1:
                    #                 # Copy file to "good" folder
                    print("good", score)
                    document = {"sku":sku,"unit_id":entry.name,"status": "good"}
                    self.coll2.insert_one(document)
                    src_path = entry.path
                    dst_path = os.path.join(self.folder_path, "good", entry.name)
                    gd = dst_path
                    dst_path2 = os.path.join(self.folder_path, "bad", entry.name)
                    bd = dst_path2
                    shutil.copyfile(src_path, dst_path)

                else:
                    flag = 1
                    print("bad", score)
                    # Copy file to "bad" folder
                    document = {"sku":sku,"unit_id":entry.name,"status": "bad"}
                    self.coll2.insert_one(document)
                    src_path = entry.path
                    dst_path = os.path.join(self.folder_path, "bad", entry.name)
                    bd = dst_path
                    cv2.imwrite(dst_path, after)
                    shutil.copyfile(src_path, dst_path)
                    # The diff image contains the actual image differences between the two images
                    # and is represented as a floating point data type in the range [0,1]
                    # so we must convert the array to 8-bit unsigned integers in the range
                    # [0,255] before we can use it with OpenCV
                    diff = (diff * 255).astype("uint8")

                    # # # Threshold the difference image, followed by finding contours to
                    # # # obtain the regions of the two input images that differ
                    thresh = cv2.threshold(
                        diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
                    )[1]
                    contours = cv2.findContours(
                        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                    )
                    contours = contours[0] if len(contours) == 2 else contours[1]

                    mask = np.zeros(before.shape, dtype="uint8")
                    filled_after = after.copy()

                    for c in contours:
                        area = cv2.contourArea(c)
                        if area > 40:
                            x, y, w, h = cv2.boundingRect(c)
                            cv2.rectangle(
                                before, (x, y), (x + w, y + h), (36, 255, 12), 2
                            )
                            cv2.rectangle(
                                after, (x, y), (x + w, y + h), (36, 255, 12), 2
                            )
                            cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
                            cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)
                    # cv2.imwrite('output.jpg', after)

                    print("bad", score)
                    src_path = entry.path
                    dst_path = os.path.join(self.folder_path, "bad", entry.name)
                    #if flag == 1:
                    #    bd = dst_path
                    cv2.imwrite(dst_path, after)
                    shutil.copyfile(src_path, dst_path)
                    #print(bd)
                    # src_path = entry.path
                    # dst_path = os.path.join(self.folder_path, "bad", entry.name)
                    # bd = dst_path
                    # cv2.imwrite(dst_path, after)
                    # shutil.copyfile(src_path, dst_path)
        #print(bd)
        tab1(self)


def tab1(self):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["ImageCP"]
    coll = db["table"]
    last_added_doc = coll.find_one(sort=[("_id", pymongo.DESCENDING)])

    file1 = last_added_doc["table"]
    self.folder_path1 = os.path.join(os.getcwd(), file1)
    bd= os.path.join(self.folder_path1, "bad")
    gd = os.path.join(self.folder_path1, "good")
    al = os.path.join(self.folder_path1, "all")

    #print("yeet")
    app = QApplication(sys.argv)
    t = TabWidget(al, gd, bd)
    t.show()
    sys.exit(app.exec_())

# if __name__ == "__main__":
#     app = QApplication([])
#     parent_widget = QtWidgets.QWidget()
#     app.exec()
#     y = QFileDialog.getExistingDirectory(parent_widget, "Open Folder")
#     x = ImageSimilarity(y)
#     x.calculate_similarity_scores(r"C:\Users\senpronics\Documents\SKU\units\images\bottle1.jpg")
