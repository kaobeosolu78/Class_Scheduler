from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QFormLayout, QLineEdit, QPushButton, QMainWindow, QAction, QListWidget
from Start import load_obj, save_obj, Course
import sys


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



class Home_Screen(MainWindow):
    def __init__(self):
        self.calendars = load_obj("calendars")
        self.raw_data = load_obj("raw_data")

        self.check_past_exam()

        super().__init__()
        self.initUI()
        self.finish("Schedule")
        self.add_menus(["new", "edit"])

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

    def edit(self):
        self.next = Edit_init(self.raw_data)

    def check_past_exam(self):
        passed_exams = {}
        for class_ in list(self.raw_data.keys()):
            passed_exams[class_] = []
            for ind,exam in enumerate(self.raw_data[class_]["Exam Dates"]):
                if datetime.datetime.today() > exam+datetime.timedelta(days=7):
                    passed_exams[class_].append((exam,ind))



class SetClasses(MainWindow):
    def __init__(self, class_data={"Class Name":"", "Exam Number":"", "Rest Days":"", "Exam Dates":[]}):#, editing=False):
        super().__init__()


        self.class_data = class_data
        # self.editing = editing

        self.add_labels()
        self.add_inputs()
        self.add_buttons("submit", (3, 0))
        if self.editing:
            self.add_buttons("delete", (3, 1))
        self.finish("Schedule")

    def add_labels(self):
        [self.grid.addWidget(QLabel(label_name), label_ind, 0) for label_ind, label_name in enumerate(["Class Name: ",
                                                                                         "Number of Exams: ",
                                                                                         "Rest Days after Exam: "])]

    def add_inputs(self):
        for input_ind, input_name in enumerate(["Class Name", "Exam Number", "Rest Days"]):
            self.class_data[input_name] = QLineEdit(str(self.class_data[input_name]))
            self.grid.addWidget(self.class_data[input_name], input_ind, 1)

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
        save_obj("calendars", cal)

        raw = load_obj("raw_data")
        del raw[self.class_data["Class Name"]]
        save_obj("raw_data", raw)



    # test = Course("Physics", [datetime.date(2020,6,29),datetime.date(2020,6,4),datetime.date(2020,7,7),
    # datetime.date(2020,7,28),datetime.date(2020,8,11)], {"Electrostatics":[0,651,675],
    # "Electric Fields" : [0,676,708], "Electric Potential" : [0,709,736], "Capacitors" : [0,737,764], "Current and Resistance" : [1,765,794], "Direct Current" : [1,795,818], "Magnetism" : [1,819,844], "Magnetic Fields" : [1,845,874], "Electromagnetic Induction" : [1,875,906], "EM Oscillations" : [2,907,938], "Electromagnetic Waves" : [2,939,970], "Geometric Optics" : [2,971,1002], "Special Relativity" : [3,1072,1107]}, 2)

class AddChapters(MainWindow):

    def __init__(self, all_chapter_info={}):
        super().__init__()

        self.all_chapter_info = all_chapter_info
        self.inputs = [QLineEdit() for temp in range(4)]

        self.add_layouts()
        self.add_labels()
        self.add_inputs()
        self.add_button("submit", (4, 0), "left_grid")
        self.add_button("delete", (4, 1), "left_grid")
        self.add_button("done", (1, 0), "right_grid")
        self.add_menus("clear")
        self.add_listbox()
        self.finish("Add Chapter")

    # gui mods
    def add_layouts(self):
        for layout_ind, layout_name in enumerate(["left_grid", "right_grid"]):
            self.__dict__[layout_name] = QGridLayout()
            self.grid.addLayout(self.__dict__[layout_name], 0, layout_ind)
        self.left_grid.setVerticalSpacing(52)

    def add_labels(self):
        for label_ind, label_name in enumerate(["Chapter Name:", "Exam Number:", "Start Page:", "Stop Page"]):
                self.left_grid.addWidget(QLabel(label_name), label_ind, 0)# name, exam #, start-stop pgs

    def add_inputs(self):
        [self.left_grid.addWidget(line, line_ind, 1) for line_ind, line in enumerate(self.inputs)]

    def add_listbox(self):
        self.listbox = QListWidget()
        self.listbox.clicked.connect(self.load_chapter_info)
        self.listbox.setMaximumHeight(302)
        self.right_grid.addWidget(self.listbox, 0, 0)


    # helper funcs
    def store_chapter(self):
        chapter_info = [line.text() for line in self.inputs]
        self.all_chapter_info[chapter_info[0]] = chapter_info[1:]
        (self.add_to_listbox(chapter_info[0]), self.set_input_text(["", "", "", ""]))

    def add_to_listbox(self, chapter_title):
        self.listbox.insertItem(self.listbox.count(), chapter_title)

    def set_input_text(self, chapter_info):
        for line, text in zip(self.inputs, chapter_info):
            line.setText(text)

    # buttons
    def submit(self):
        self.store_chapter()
        self.set_input_text([""]*4)

    def delete(self):
        del self.all_chapter_info[self.listbox.currentItem().text()]
        if self.listbox.currentIndex().row() != -1:  # fiiiiiix up
            self.listbox.takeItem(self.listbox.currentIndex().row())
        self.set_input_text([""]*4)

    def done(self):
        self.close()
        save_obj("temp_name", self.all_chapter_info)


    def clear(self):
        self.listbox.clear()
        self.all_chapter_info = {}

    def load_chapter_info(self):
        self.set_input_text([self.listbox.currentItem().text()]+self.all_chapter_info[self.listbox.currentItem().text()])





def main():
    app = QApplication(sys.argv)
    a = AddChapters()
    sys.exit(app.exec_())

main()