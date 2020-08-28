from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QFormLayout, QLineEdit, QPushButton, QMainWindow, QAction, QListWidget
import sys
from math import ceil
from Start import load_obj, Course
import datetime
import pickle
import Upload



# def pickle_output(file_name="file"):
#     def decorate(func):
#         def pickle_out(*arg):
#             out = func(*arg)
#             pick_out = open("{}.pkl".format(file_name), "wb")
#             pickle.dump(out, pick_out, pickle.HIGHEST_PROTOCOL)
#             pick_out.close()
#             return out
#         return pickle_out
#     return decorate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        self.grid = QGridLayout()


    def finish(self, title, x_dim=500, y_dim=400):
        self.window.setLayout(self.grid)
        self.setGeometry(1300, 300, x_dim, y_dim)
        self.setWindowTitle(title)
        self.show()


class Edit_init(MainWindow):
    def __init__(self, rd):
        self.raw_data = rd

        super().__init__()
        self.initUI()
        self.finish("Schedule")

    def initUI(self):
        # label
        title = QLabel("Which Course Would You Like to Edit:")
        self.grid.addWidget(title,0,0)

        # input
        self.lb = QListWidget()

        for k in range(len(list(self.raw_data.keys()))):
            self.lb.insertItem(k, list(self.raw_data.keys())[k])

        self.lb.clicked.connect(self.continu)
        self.grid.addWidget(self.lb,1,0)


    def continu(self):
        item = self.lb.currentItem().text()
        self.close()
        SetClasses(self.raw_data[item], True)


class SetClasses(MainWindow):
    def __init__(self, class_data={"Class Name":"", "Exam Number":"", "Rest Days":"", "Exam Dates":[],
                                   "Chapter Number":"", "Chapters":{}}, editing=False):
        self.class_data = class_data
        self.editing = editing

        super().__init__()
        self.add_labels()
        self.add_inputs()
        self.add_buttons()
        self.finish("Schedule")

    def add_labels(self):
        [self.grid.addWidget(QLabel(label_name), label_ind, 0) for label_ind, label_name in enumerate(["Class Name: ",
                                                                                         "Number of Exams: ",
                                                                                         "Rest Days after Exam: "])]

    def add_inputs(self):
        for input_ind, input_name in enumerate(["Class Name", "Exam Number", "Rest Days"]):
            self.class_data[input_name] = QLineEdit(str(self.class_data[input_name]))
            self.grid.addWidget(self.class_data[input_name], input_ind, 1)

    def add_buttons(self):  # var, getattr, coord
        submit = QPushButton("Submit")
        submit.clicked.connect(lambda: self.submit())
        self.grid.addWidget(submit, 3, 0)

        if self.editing:
            delete = QPushButton("Delete")
            delete.clicked.connect(lambda: self.delete())
            self.grid.addWidget(delete, 3, 1)

    def submit(self): # fix up
        self.class_data["Class Name"] = self.class_data["Class Name"].text()
        self.class_data["Exam Number"] = int(self.class_data["Exam Number"].text())  # implement custom error message
        self.class_data["Rest Days"] = int(self.class_data["Rest Days"].text())
        self.close()
        self.next = SetExams(self.class_data, self.editing)

    def delete(self):
        self.close()

        cal = load_obj("calendars")
        del cal[self.class_data["Class Name"]]
        pick_out = open("calendars.pkl", "wb")
        pickle.dump(cal, pick_out, pickle.HIGHEST_PROTOCOL)
        pick_out.close()

        raw = load_obj("raw_data")
        del raw[self.class_data["Class Name"]]
        pick_out = open("raw_data.pkl", "wb")
        pickle.dump(raw, pick_out, pickle.HIGHEST_PROTOCOL)
        pick_out.close()


class SetExams(MainWindow):
    def __init__(self, class_data, editing=False):#class_name, exam_num):
        self.class_data = class_data
        self.editing = editing

        super().__init__()
        self.add_labels()
        self.add_inputs()
        self.finish("Schedule")
        self.add_buttons()

    def add_labels(self):
        [self.grid.addWidget(QLabel(label_name), label_ind, 2) for label_ind, label_name in enumerate(["Start Date: ",
                                                                                         "Number of Chapters: ",
                                                                                         "Example Date Format: 1/20/2020"])]

    def add_inputs(self):
        if not self.editing:  # add error for empty
            date_temp = ["" for k in range(self.class_data["Exam Number"])]
        else:
            date_temp = [self.class_data["Exam Dates"][k].strftime("%m/%d/%Y") if k < len(self.class_data["Exam Dates"])
                         else "" for k in range(self.class_data["Exam Number"])]  # add window destructor
        self.class_data["Exam Dates"] = self.class_data["Exam Dates"][:len(date_temp)]  # improve

        self.class_data["Chapter Number"] = QLineEdit(str(self.class_data["Chapter Number"]))
        self.grid.addWidget(self.class_data["Chapter Number"], 1, 3)
        for date_ind, date in enumerate(date_temp):
            self.grid.addWidget(QLabel(f"Exam {date_ind+1} Date: "), date_ind, 0)
            try:
                self.class_data["Exam Dates"][date_ind] = QLineEdit(date)
            except:
                self.class_data["Exam Dates"].append(QLineEdit(date))

            (self.grid.addWidget(self.class_data["Exam Dates"][date_ind], date_ind, 1),
             self.class_data["Exam Dates"][date_ind].setFixedWidth(87))

    def add_buttons(self):
        submit = QPushButton("Submit")
        submit.clicked.connect(lambda: self.submit())
        self.grid.addWidget(submit, self.class_data["Exam Number"]+1, 0)

    def submit(self):
        self.class_data["Exam Dates"] = [datetime.datetime.strptime(date.text(), "%m/%d/%Y")
                                   for date in self.class_data["Exam Dates"]]
        self.class_data["Chapter Number"] = int(self.class_data["Chapter Number"].text())
        self.close()
        self.next = Set_Chapters(self.class_data)


class Set_Chapters(MainWindow):
    def __init__(self, class_data):
        self.class_data = class_data

        super().__init__()
        self.initUI()
        self.add_buttons()

    def initUI(self):
        # input
        count = 0
        count3 = 0
        self.temp = []
        for exam_index, k in enumerate(range(0, self.class_data["Exam Number"]*2, 2)): # exam num
            exam_index += 1
            self.grid.addWidget(QLabel("Exam {}".format(exam_index)), 0, k+1)
            for j in range(1, 3*ceil(self.class_data["Chapter Number"]/self.class_data["Exam Number"])+1):
                count += 1
                if count == 1:
                    count3 += 1
                    title = QLabel("Chapter {} Name: ".format(count3))
                    entry = QLineEdit(list(self.class_data["Chapters"].keys())[count3-1])
                if count == 2:
                    title = QLabel("Start Page: ")
                    entry = QLineEdit(str(self.class_data["Chapters"][list(self.class_data["Chapters"].keys())[count3-1]][1]))
                if count == 3:
                    count = 0
                    title = QLabel("End Page: ")
                    entry = QLineEdit(str(self.class_data["Chapters"][list(self.class_data["Chapters"].keys())[count3-1]][2]))
                self.grid.addWidget(title, j, k)
                self.temp.append(entry)
                self.grid.addWidget(entry, j, k+1)

    def add_buttons(self):
        submit = QPushButton("Submit")
        submit.clicked.connect(lambda: self.save())
        self.grid.addWidget(submit, j+1, k)

    def save(self):
        self.close()
        exam = 0
        self.class_data["Chapters"] = {}
        for k in range(0, len(self.temp), 3):
            if k != 0 and k % (3*ceil(self.class_data["Chapter Number"]/self.class_data["Exam Number"])) == 0:
                exam += 1
            self.class_data["Chapters"][self.temp[k].text()] = [exam, int(self.temp[k+1].text()), int(self.temp[k+2].text())]

        course = Course(self.class_data["Class Name"],self.class_data["Exam Dates"],self.class_data["Chapters"],self.class_data["Rest Days"])

        rd = load_obj("raw_data")
        rd[self.class_data["Class Name"]] = self.class_data
        pick_out = open("raw_data.pkl", "wb")
        pickle.dump(rd, pick_out, pickle.HIGHEST_PROTOCOL)
        pick_out.close()

class Home_Screen(MainWindow):
    def __init__(self):
        self.calendars = load_obj("calendars")
        self.raw_data = load_obj("raw_data")

        self.check_past_exam()

        super().__init__()
        self.initUI()
        self.finish("Schedule")

    def initUI(self):
        # labels
        self.grid.addWidget(QLabel("Upcoming\nItems..."), 0, 0)

        temp = {}
        count1 = 1
        for clas in list(self.calendars.keys()):
            self.grid.addWidget(QLabel("-----"+clas+"-----"),1,count1)
            temp[clas] = {}
            count2 = 0
            for exam in list(self.calendars[clas].keys()):
                if count2 == 5: break
                for chap in list(self.calendars[clas][exam].keys()):
                    for date in self.calendars[clas][exam][chap]:
                        if date >= datetime.date.today() and count2 != 5:
                            self.grid.addWidget(QLabel(str(date.month)+"/"+str(date.day)+"/"+str(date.year)+":"), count2+2, count1-1)
                            self.grid.addWidget(QLabel(chap+"        "), count2+2, count1)
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

    def newClass(self):
        self.next = SetClasses()

    def editClass(self):
        self.next = Edit_init(self.raw_data)

    def check_past_exam(self):
        passed_exams = {}
        for class_ in list(self.raw_data.keys()):
            passed_exams[class_] = []
            for ind,exam in enumerate(self.raw_data[class_]["Exam Dates"]):
                if datetime.datetime.today() > exam+datetime.timedelta(days=7):
                    passed_exams[class_].append((exam,ind))


def main():
    app = QApplication(sys.argv)
    a = Home_Screen()
    # sg = Set_Chapters({"Chapter Number":22, "Exam Number":3})
    sys.exit(app.exec_())

main()