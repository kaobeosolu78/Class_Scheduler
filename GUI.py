from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QFormLayout, QLineEdit, QPushButton, QMainWindow, QAction, QListWidget
import sys
from math import ceil
from Start import load_obj, Course
import datetime
import pickle
import Upload


class Edit_init(QWidget):
    def __init__(self, rd):
        self.raw_data = rd

        super().__init__()
        self.initUI()

    def initUI(self):
        # layout
        grid = QGridLayout()

        # label
        title = QLabel("Which Course Would You Like to Edit:")
        grid.addWidget(title,0,0)

        # input
        self.lb = QListWidget()

        for k in range(len(list(self.raw_data.keys()))):
            self.lb.insertItem(k, list(self.raw_data.keys())[k])

        self.lb.clicked.connect(self.continu)
        grid.addWidget(self.lb,1,0)

        self.setLayout(grid)
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Schedule')
        self.show()

    def continu(self):
        item = self.lb.currentItem().text()
        self.close()
        Set_Classes(self.raw_data[item], True)


class Set_Classes(QWidget):
    def __init__(self, data = {"Class Name":"", "Exam Number":"", "Rest Days":"", "Exam Dates":[], "Chapter Number":"", "Chapters":{}}, edit = False):
        self.data = data
        self.edit = edit

        super().__init__()
        self.initUI()

    def initUI(self):

        # layout
        grid = QGridLayout()

        # labels
        title = QLabel("Class Name: ")
        grid.addWidget(title, 0, 0)

        title = QLabel("Number of Exams: ")
        grid.addWidget(title, 1, 0)

        title = QLabel("Rest Days after Exam: ")
        grid.addWidget(title, 2, 0)


        # forms
        self.class_name = QLineEdit(self.data["Class Name"])
        grid.addWidget(self.class_name, 0, 1)

        self.exam_num = QLineEdit(str(self.data["Exam Number"]))
        grid.addWidget(self.exam_num, 1, 1)

        self.rest_days = QLineEdit(str(self.data["Rest Days"]))
        grid.addWidget(self.rest_days, 2, 1)

        # buttons
        submit = QPushButton("Submit")
        submit.clicked.connect(lambda: self.next())
        grid.addWidget(submit, 3, 0)

        # delete
        if self.edit:
            delete = QPushButton("Delete")
            delete.clicked.connect(lambda: self.delete())
            grid.addWidget(delete, 3, 1)

        # general settings
        self.setLayout(grid)
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Schedule')
        self.show()

    def next(self):
        self.close()
        self.data["Class Name"] = self.class_name.text()
        self.data["Exam Number"] = int(self.exam_num.text())
        self.data["Rest Days"] = int(self.rest_days.text())
        self.next = Set_Exams(self.data)

    def delete(self):
        self.close()

        cal = load_obj("calendars")
        del cal[self.data["Class Name"]]
        pick_out = open("calendars.pkl", "wb")
        pickle.dump(cal, pick_out, pickle.HIGHEST_PROTOCOL)
        pick_out.close()

        raw = load_obj("raw_data")
        del raw[self.data["Class Name"]]
        pick_out = open("raw_data.pkl", "wb")
        pickle.dump(raw, pick_out, pickle.HIGHEST_PROTOCOL)
        pick_out.close()

class Set_Exams(QWidget):
    def __init__(self, data):#class_name, exam_num):
        self.data = data

        super().__init__()
        self.initUI()

    def initUI(self):
        # layout
        grid = QGridLayout()

        # input
        title = QLabel("Start Date: ")
        grid.addWidget(title, 0, 2)
        title = QLabel("Number of Chapters: ")
        grid.addWidget(title, 1, 2)
        title = QLabel("Example Date Format: 1/20/2020")
        grid.addWidget(title, 2, 2)
        # self.data["Exam Dates"]
        temp = [QLineEdit(self.data["Exam Dates"][0].strftime("%m/%d/%Y"))]
        temp[0].setFixedWidth(87)
        grid.addWidget(temp[0], 0, 3)
        self.data["Chapter Number"] = QLineEdit(str(self.data["Chapter Number"]))
        grid.addWidget(self.data["Chapter Number"], 1, 3)

        for k in range(self.data["Exam Number"]):
            title = QLabel("Exam {} Date: ".format(k+1))
            grid.addWidget(title, k, 0)
            form = QLineEdit(self.data["Exam Dates"][k].strftime("%m/%d/%Y"))
            form.setFixedWidth(87)
            grid.addWidget(form, k, 1)
            temp.append(form)
        self.data["Exam Dates"] = temp

        # buttons
        submit = QPushButton("Submit")
        submit.clicked.connect(lambda: self.next())
        grid.addWidget(submit, self.data["Exam Number"]+1, 0)

        # general settings
        self.setLayout(grid)
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Schedule')
        self.show()

    def next(self):
        self.close()
        self.data["Exam Dates"] = [datetime.datetime.strptime(date.text(),"%m/%d/%Y") for date in self.data["Exam Dates"]]
        self.data["Chapter Number"] = int(self.data["Chapter Number"].text())
        self.next = Set_Chapters(self.data)


class Set_Chapters(QWidget):
    def __init__(self, data):
        self.data = data

        super().__init__()
        self.initUI()

    def initUI(self):
        # layout
        grid = QGridLayout()

        # input
        count = 0
        count2 = 0
        count3 = 0
        self.temp = []
        for k in range(0, self.data["Exam Number"]*2, 2): # exam num
            count2 += 1
            title = QLabel("Exam {}".format(count2))
            grid.addWidget(title, 0, k+1)
            for j in range(1, 3*ceil(self.data["Chapter Number"]/self.data["Exam Number"])+1):
                count += 1
                if count == 1:
                    count3 += 1
                    title = QLabel("Chapter {} Name: ".format(count3))
                    entry = QLineEdit(list(self.data["Chapters"].keys())[count3-1])
                if count == 2:
                    title = QLabel("Start Page: ")
                    entry = QLineEdit(str(self.data["Chapters"][list(self.data["Chapters"].keys())[count3-1]][1]))
                if count == 3:
                    count = 0
                    title = QLabel("End Page: ")
                    entry = QLineEdit(str(self.data["Chapters"][list(self.data["Chapters"].keys())[count3-1]][2]))
                grid.addWidget(title, j, k)
                self.temp.append(entry)
                grid.addWidget(entry, j, k+1)

        # buttons
        submit = QPushButton("Submit")
        submit.clicked.connect(lambda: self.save())
        grid.addWidget(submit, j+1, k)

        # general settings
        self.setLayout(grid)
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Schedule')
        self.show()

    def save(self):
        self.close()
        exam = 0
        self.data["Chapters"] = {}
        for k in range(0, len(self.temp), 3):
            if k != 0 and k % (3*ceil(self.data["Chapter Number"]/self.data["Exam Number"])) == 0:
                exam += 1
            self.data["Chapters"][self.temp[k].text()] = [exam, int(self.temp[k+1].text()), int(self.temp[k+2].text())]

        course = Course(self.data["Class Name"],self.data["Exam Dates"],self.data["Chapters"],self.data["Rest Days"])

        rd = {}#load_obj("raw_data")
        rd[self.data["Class Name"]] = self.data
        pick_out = open("raw_data.pkl", "wb")
        pickle.dump(rd, pick_out, pickle.HIGHEST_PROTOCOL)
        pick_out.close()

class Home_Screen(QMainWindow):
    def __init__(self):
        self.calendars = load_obj("calendars")
        self.raw_data = load_obj("raw_data")

        super().__init__()
        self.initUI()

    def initUI(self):
        # layout
        wid = QWidget(self)
        self.setCentralWidget(wid)
        grid = QGridLayout()

        # labels
        title = QLabel("Upcoming\nItems...")
        grid.addWidget(title, 0, 0)

        temp = {}
        count1 = 1
        for clas in list(self.calendars.keys()):
            title = QLabel("-----"+clas+"-----")
            grid.addWidget(title,1,count1)
            temp[clas] = {}
            count2 = 0
            for exam in list(self.calendars[clas].keys()):
                if count2 == 5: break
                for chap in list(self.calendars[clas][exam].keys()):
                    for date in self.calendars[clas][exam][chap]:
                        if date >= datetime.date.today() and count2 != 5:
                            title = QLabel(str(date.month)+"/"+str(date.day)+"/"+str(date.year)+":")
                            grid.addWidget(title, count2+2, count1-1)
                            title = QLabel(chap+"        ")
                            grid.addWidget(title, count2+2, count1)
                            count2 += 1
            count1 += 2

        # menus
        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")

        new = QAction("New Class", self)
        new.triggered.connect(lambda: self.newClass())
        filemenu.addAction(new)

        edit = QAction("Edit Class", self)
        edit.triggered.connect(lambda: self.editClass())
        filemenu.addAction(edit)

        # general settings
        wid.setLayout(grid)
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Schedule')
        self.show()

    def newClass(self):
        self.next = Set_Classes()

    def editClass(self):
        self.next = Edit_init(self.raw_data)

def main():
    app = QApplication(sys.argv)
    a = Home_Screen()
    # sg = Set_Chapters({"Chapter Number":22, "Exam Number":3})
    sys.exit(app.exec_())

main()