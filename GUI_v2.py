from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QFormLayout, QLineEdit, QPushButton, QMainWindow, QAction, QListWidget
from Start import load_obj, save_obj, Course
import datetime
import sys
import abc



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

    def add_button(self, name, coords, layout="grid"):
        button = QPushButton(name.title())
        button.clicked.connect(lambda: getattr(self, name)())
        self.__dict__[layout].addWidget(button, coords[0], coords[1])

    def add_menus(self, names):
        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")

        for name in names:
            menu = QAction(name.title(), self)
            menu.triggered.connect(lambda: getattr(self, name)())
            filemenu.addAction(menu)



class ListEntry(MainWindow):
    def __init__(self, params):
        super().__init__()

        # self.stored_info = stored_info
        self.inputs = [QLineEdit() for temp in range(params["input number"])]

        self.add_layouts(params["layout size"])
        self.add_labels(params["label names"])
        self.add_inputs()
        self.add_button(params["button1 name"], params["button1 coords"], "left_grid")  # add loop
        self.add_button(params["button2 name"], params["button2 coords"], "left_grid")
        self.add_button(params["button3 name"], params["button3 coords"], "right_grid")
        self.add_listbox()
        # self.add_menus(["clear"])


    # gui mods
    def add_layouts(self, grid_spacing):
        for layout_ind, layout_name in enumerate(["left_grid", "right_grid"]):
            self.__dict__[layout_name] = QGridLayout()
            self.grid.addLayout(self.__dict__[layout_name], 0, layout_ind)
        self.left_grid.setVerticalSpacing(grid_spacing)

    def add_labels(self, labels):
        for label_ind, label_name in enumerate(labels):
            self.left_grid.addWidget(QLabel(label_name), label_ind, 0)

    def add_inputs(self):
        [self.left_grid.addWidget(line, line_ind, 1) for line_ind, line in enumerate(self.inputs)]
        
    def add_listbox(self):
        self.listbox = QListWidget()
        self.listbox.clicked.connect(self.load_info)
        self.listbox.setMaximumHeight(302)
        self.right_grid.addWidget(self.listbox, 0, 0)


    # helper funcs
    def add_to_listbox(self, chapter_title):
        self.listbox.insertItem(self.listbox.count(), chapter_title)

    def set_input_text(self, chapter_info):
        for line, text in zip(self.inputs, chapter_info):
            line.setText(text)

    @abc.abstractmethod
    def store_info(self):
        input_text = [line.text() for line in self.inputs]
        self.add_to_listbox(input_text[0])
        self.set_input_text([""]*4)
        return input_text

    # buttons
    @abc.abstractmethod
    def load_info(self):
        pass

    def submit(self):
        self.store_info()
        self.set_input_text([""]*4)

    def delete(self):
        del self.stored_info[self.listbox.currentItem().text()]
        if self.listbox.currentIndex().row() != -1:  # add dialog with error
            self.listbox.takeItem(self.listbox.currentIndex().row())
        self.set_input_text([""]*4)


class Home_Screen(MainWindow):
    def __init__(self):
        super().__init__()


        self.calendars = load_obj("calendars")
        self.raw_data = load_obj("raw_data")

        # self.check_past_exam()

        self.initUI()
        self.finish("Schedule")
        self.add_menus(["new"])  # , "edit"])

    def initUI(self):
        # labelsedit
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

    def new(self):
        self.next = SetClasses()
    #
    # def edit(self):
    #     self.next = Edit_init(self.raw_data)

    # def check_past_exam(self):
    #     passed_exams = {}
    #     for class_ in list(self.raw_data.keys()):
    #         passed_exams[class_] = []
    #         for ind,exam in enumerate(self.raw_data[course_]["Exam Dates"]):
    #             if datetime.datetime.today() > exam+datetime.timedelta(days=7):
    #                 passed_exams[class_].append((exam,ind))


class AddCourses(ListEntry):
    def __init__(self):
        super().__init__({"input number": 2, "layout size": 129, "label names": ["Course Name:", "Number of Exams:"],
                          "button1 name": "submit", "button1 coords": (2, 0), "button2 name": "delete",
                          "button2 coords": (2, 1), "button3 name": "next", "button3 coords": (1, 0)})

        self.stored_info = {}

        self.finish("Add Course")

    def store_info(self):
        course_info = super().store_info()
        self.stored_info[course_info[0]] = {"Exam Dates": {}, "Number of Exams": course_info[1]}

    def load_info(self):
        self.set_input_text([self.listbox.currentItem().text(),
                             self.stored_info[self.listbox.currentItem().text()]["Number of Exams"]])

    def next(self):
        print()
        if self.listbox.currentItem():
            AddDates(self.stored_info, self.listbox.currentItem().text())
        else:
            exit()# add error dialog


    # test = Course("Physics", [datetime.date(2020,6,29),datetime.date(2020,6,4),datetime.date(2020,7,7),
    # datetime.date(2020,7,28),datetime.date(2020,8,11)], {"Electrostatics":[0,651,675],
    # "Electric Fields" : [0,676,708], "Electric Potential" : [0,709,736], "Capacitors" : [0,737,764], "Current and Resistance" : [1,765,794], "Direct Current" : [1,795,818], "Magnetism" : [1,819,844], "Magnetic Fields" : [1,845,874], "Electromagnetic Induction" : [1,875,906], "EM Oscillations" : [2,907,938], "Electromagnetic Waves" : [2,939,970], "Geometric Optics" : [2,971,1002], "Special Relativity" : [3,1072,1107]}, 2)

class AddDates(ListEntry):

    def __init__(self, stored_info, class_name):
        super().__init__()


class AddChapters(ListEntry):

    def __init__(self, stored_info):
        super().__init__({"input number": 4, "layout size": 52, "label names": ["Chapter Name:", "Exam Number:",
                          "Start Page:", "Stop Page"], "button1 name": "submit", "button1 coords": (4, 0),
                          "button2 name": "delete", "button2 coords": (4, 1), "button3 name": "done",
                          "button3 coords": (1, 0)})

        self.stored_info = stored_info

        self.finish("Add Chapter")

    # helper funcs
    def store_info(self):
        chapter_info = super().store_info() # fix to incorporate prev win
        self.stored_info[chapter_info[0]] = chapter_info[1:]

    def load_info(self):
        self.set_input_text([self.listbox.currentItem().text()]+self.stored_info[self.listbox.currentItem().text()])

    def done(self):
        save_obj("temp_name", self.stored_info) # improve
        self.close()

    def clear(self):
        self.listbox.clear()
        self.stored_info = {}





def main():
    app = QApplication(sys.argv)
    a = AddCourses()
    # a = AddChapters({})
    sys.exit(app.exec_())

main()