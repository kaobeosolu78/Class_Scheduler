from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QFormLayout, QLineEdit, QPushButton, QMainWindow, QAction, QListWidget
from Start import load_obj, save_obj, Course
import datetime
from operator import attrgetter
import sys
import abc
import time
# cheeeeck function calls on composition vs inheritance
# add decorator for setting current_type
# check out viability of descriptor implementation in some vars
# implement current_type = self.__class__.__name__[3:-1].lower()
# relearn args+kwargs


class CourseSchedule:
    def __init__(self, course_name, exam_number):
        self.course_name = course_name
        self.exam_number = exam_number  # get rid of this
        self.exam_dates = []
        self.chapters = {}

    def course_loadable(self):
        return [self.course_name, self.exam_number]

    def chapter_loadable(self, chapter_name):
        return [chapter_name] + self.chapters[chapter_name][1:]

        """
    def complex(real=0.0, imag=0.0): # Example docstring using pep
        '''Form a complex number.

        Keyword arguments:
        real -- the real part (default 0.0)
        imag -- the imaginary part (default 0.0)

        """

class GuiLayout(QMainWindow):
    def __init__(self, master):
        super().__init__()
        self.master = master

    def add_button(self, name, coords, layout, current_type):
        button = QPushButton(name.title())
        button.clicked.connect(lambda: getattr(self, name)(current_type))
        self.master.__dict__[layout].addWidget(button, coords[0], coords[1])

    def add_menus(self, names):
        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")

        for name in names:
            menu = QAction(name.title(), self)
            menu.triggered.connect(lambda: getattr(self, name)())
            filemenu.addAction(menu)

    def add_layouts(self, parent_grid, grid_spacing):  # add nother' param
        for layout_ind, layout_name in enumerate(["left_grid", "right_grid"]):
            self.master.__dict__[layout_name] = QGridLayout()
            self.master.__dict__[parent_grid].addLayout(getattr(self.master, layout_name), 0, layout_ind)
            getattr(self.master, layout_name).setVerticalSpacing(grid_spacing)

    def add_labels(self, labels):
        for label_ind, label_name in enumerate(labels):
            self.master.left_grid.addWidget(QLabel(label_name), label_ind, 0)

    def add_inputs(self, current_type):
        [self.master.left_grid.addWidget(line, line_ind, 1) for line_ind, line in enumerate(getattr(self, f"{current_type}_input"))]

    def add_listbox(self, current_type):
        self.__dict__[f"{current_type}_list"] = QListWidget()
        self.__dict__[f"{current_type}_list"].clicked.connect(self.load_info)
        self.__dict__[f"{current_type}_list"].setMaximumHeight(302)
        self.master.right_grid.addWidget(self.__dict__[f"{current_type}_list"], 0, 0)

class GuiFunctions(GuiLayout):
    def __init__(self, master, params):# fix
        super().__init__(master)


        # self.inputs = [QLineEdit() for temp in range(params["input number"])]
        #
        # self.add_layouts(params["parent grid"])#params["layout size"])
        # self.add_labels(params["label names"])
        # self.add_inputs()
        # self.add_button(params["button1 name"], params["button1 coords"], "left_grid")  # add loop
        # self.add_button(params["button2 name"], params["button2 coords"], "left_grid")
        # self.add_button(params["button3 name"], params["button3 coords"], "right_grid")
        # self.add_listbox()
        # self.add_menus(["clear"])

    # helper funcs
    def add_to_listbox(self, word, current_type):
        getattr(self, f"{current_type}_list").insertItem(getattr(self, f"{current_type}_list").count(), word)
        # attrgetter(f"{current_type}.{current_type}_list")(self.master).insertItem(getattr(self, f"{current_type}_list").count(), word)

    def set_input_text(self, text_list, current_type):
        for line, text in zip(attrgetter(f"{current_type}.{current_type}_input")(self.master), text_list):
            line.setText(text)

    @abc.abstractmethod
    def store_info(self, current_type):
        input_text = [line.text() for line in getattr(self, f"{current_type}_input")]
        self.add_to_listbox(input_text[0], current_type)
        return input_text

    # buttons
    def add(self, current_type):
        self.store_info()
        self.set_input_text([""]*4, current_type)

    @abc.abstractmethod
    def delete(self, types):
        input_number = [4, 1, 3][-len(types):]
        attrgetter(f"{types[0]}.{types[0]}_list")(self.master).takeItem(attrgetter(f"{types[0]}.{types[0]}_list")(self.master).currentRow())
        [self.set_input_text([""]*input_number, current_type) for input_number, current_type in zip(input_number, types)]
        clear_list = types[1:]
        if len(types) == 1:
            clear_list = types
        for current_type in clear_list:
            current_list = attrgetter(f"{current_type}.{current_type}_list")(self.master)
            current_list.clear()


class Home_Screen(GuiFunctions):
    def __init__(self, master):
        super().__init__(master)


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


class AddCourses(GuiFunctions):
    def __init__(self, master):
        super().__init__(master, {"input number": 2, "layout size": 129, "label names": ["Course Name:", "Exam Number:"],
                          "button1 name": "add", "button1 coords": (2, 0), "button2 name": "delete",
                          "button2 coords": (2, 1), "button3 name": "next", "button3 coords": (1, 0), "parent grid":
                          "course_grid"})

        self.course_input = [QLineEdit() for temp in range(2)]

        self.add_layouts("course_grid", 100)
        self.add_labels(["Course Name:", "Exam Number:"])
        self.add_inputs("course")
        self.add_button("add", (2, 0), "left_grid", "course")  # add loop
        self.add_button("delete", (2, 1), "left_grid", "course")
        self.add_listbox("course")

    def store_info(self):
        course_info = super().store_info("course")
        self.master.stored_info[course_info[0]] = CourseSchedule(course_info[0], course_info[1])  # add error dialog or descriptor
        # self.master.stored_info[course_info[0]] = {}

    def load_info(self):
        self.set_input_text(self.master.stored_info[self.master.get_current_selection("course")].course_loadable(), "course")
        self.master.save_list(True)

    def delete(self, *args):
        del self.master.stored_info[self.master.get_current_selection("course")]
        super().delete(["course", "date", "chapter"])


    # test = Course("Physics", [datetime.date(2020,6,29),datetime.date(2020,6,4),datetime.date(2020,7,7),
    # datetime.date(2020,7,28),datetime.date(2020,8,11)], {"Electrostatics":[0,651,675],
    # "Electric Fields" : [0,676,708], "Electric Potential" : [0,709,736], "Capacitors" : [0,737,764], "Current and Resistance" : [1,765,794], "Direct Current" : [1,795,818], "Magnetism" : [1,819,844], "Magnetic Fields" : [1,845,874], "Electromagnetic Induction" : [1,875,906], "EM Oscillations" : [2,907,938], "Electromagnetic Waves" : [2,939,970], "Geometric Optics" : [2,971,1002], "Special Relativity" : [3,1072,1107]}, 2)

class AddDates(GuiFunctions):

    def __init__(self, master):
        super().__init__(master, {"input number": 2, "layout size": 129, "label names": ["Course Name:", "Exam Number:"],
                          "button1 name": "add", "button1 coords": (2, 0), "button2 name": "delete",
                          "button2 coords": (2, 1), "button3 name": "next", "button3 coords": (1, 0)})


        self.date_input = [QLineEdit()]
        self.not_so_current_selection = []

        self.add_layouts("date_grid", 224)
        self.add_labels(["Exam Date:"])
        self.add_inputs("date")
        self.add_button("add", (1, 0), "left_grid", "date")  # add loop
        self.add_button("delete", (1, 1), "left_grid", "date")
        self.add_listbox("date")

    # helper funcs
    def store_info(self):
        date_info = super().store_info("date")  # fix to incorporate prev window
        self.master.stored_info[self.master.get_current_selection("course")].exam_dates.append(date_info[0])

    def load_info(self):
        self.set_input_text([self.master.get_current_selection("date")], "date")
        self.master.save_list()

    def delete(self, *args):
        self.master.stored_info[self.master.get_current_selection("course")].exam_dates.remove(self.master.get_current_selection("date"))
        super().delete(["date", "chapter"])


class AddChapters(GuiFunctions):

    def __init__(self, master):
        super().__init__(master, {"input number": 4, "layout size": 52, "label names": ["Chapter Name:", "Exam Number:",
                          "Start Page:", "Stop Page"], "button1 name": "add", "button1 coords": (4, 0),
                          "button2 name": "delete", "button2 coords": (4, 1), "button3 name": "done",
                          "button3 coords": (1, 0), "listbox grid": "right_grid", "parent grid": "chapter_grid"})

        self.chapter_input = [QLineEdit() for temp in range(3)]

        self.add_layouts("chapter_grid", 27)
        self.add_labels(["Chapter Name:", "Start Page:", "Stop Page"])
        self.add_inputs("chapter")
        self.add_button("add", (4, 0), "left_grid", "chapter")  # add loop
        self.add_button("delete", (4, 1), "left_grid", "chapter")
        self.add_button("submit", (1, 1), "right_grid", "chapter")
        self.add_listbox("chapter")

    # helper funcs
    def store_info(self):
        chapter_info = super().store_info("chapter")  # fix to incorporate prev win
        exam_number = self.master.stored_info[self.master.get_current_selection("course")].exam_dates.index(self.master.get_current_selection("date"))
        self.master.stored_info[self.master.get_current_selection("course")].chapters[chapter_info[0]] = [exam_number]+chapter_info[1:]

    def load_info(self):
        self.set_input_text(self.master.stored_info[self.master.get_current_selection("course")].chapter_loadable(
                self.master.get_current_selection("chapter")), "chapter")

    def delete(self, *args):
        del self.master.stored_info[self.master.get_current_selection("course")].chapters[self.master.get_current_selection("chapter")] # add error dialog for no selection
        super().delete(["chapter"])


class Master(QMainWindow):
    def __init__(self):
        super().__init__()
        self.add_window()
        self.add_all_layouts()
        self.temp = 0

        self.stored_info = {}
        self.course = AddCourses(self)
        self.date = AddDates(self)
        self.chapter = AddChapters(self)
        self.display("test")


    def add_window(self):
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        self.main_grid = QGridLayout()

    def add_all_layouts(self):  # , grid_spacing): # add nother' param
        for layout_ind, layout_name in enumerate(["course_grid", "date_grid", "chapter_grid"]):
            self.__dict__[layout_name] = QGridLayout()
            self.main_grid.addLayout(self.__dict__[layout_name], 0, layout_ind)

    def get_current_selection(self, current_type): # solve course_list mystery
        return attrgetter(f"{current_type}.{current_type}_list")(self).currentItem().text()

    # def save_list(self, current_type):
    #     temp = self.chapter.chapter_list.count()
    #     if self.temp != self.course.not_so_current_index:
    #         previous_course_selection = self.course.not_so_current_selection[self.course.not_so_current_index-1]
    #     else:
    #         previous_course_selection = self.get_current_selection("course")
    #     for date in range(self.date.date_list.count()):
    #         self.stored_info[previous_course_selection].list_data[self.date.date_list.takeItem(0).text()] = \
    #             [self.chapter.chapter_list.takeItem(0).text() for item in range(temp)]
    #     self.load_list(current_type)
        # self.temp = self.course.not_so_current_index
        # print(self.course.not_so_current_selection[self.course.not_so_current_index-1], self.stored_info[self.course.not_so_current_selection[self.course.not_so_current_index-1]].list_data)

    def save_list(self, course_switch=False):
        if not course_switch:
            try:
                current_date = self.date.date_list.currentItem().text() # maybe replace with .index of cd
            except:
                current_date = None
        else:
            current_date = None

        for current_type in ["date", "chapter"]:
            the_list = attrgetter(f"{current_type}.{current_type}_list")(self)
            count = the_list.count()
            for k in range(count):
                the_list.takeItem(0)
        self.load_list(current_date)

    def load_list(self, current_date):  # make more efficient later

        for ind, exam_date in enumerate(self.stored_info[self.get_current_selection("course")].exam_dates):
            getattr(self, "date").add_to_listbox(exam_date, "date")
            if exam_date == current_date:
                self.date.date_list.setCurrentRow(self.stored_info[self.get_current_selection("course")].exam_dates.index(current_date))

        if current_date != None:
            date_index = self.stored_info[self.get_current_selection("course")].exam_dates.index(current_date)
            for chapter_name, chapter_info in zip(list(self.stored_info[self.get_current_selection("course")].chapters.keys()),
                                                  list(self.stored_info[self.get_current_selection("course")].chapters.values())):
                if chapter_info[0] == date_index:
                    getattr(self, "chapter").add_to_listbox(chapter_name, "chapter")

    def display(self, title, x_dim=500, y_dim=400):
        self.window.setLayout(self.main_grid)
        self.setGeometry(1300, 300, x_dim, y_dim)
        self.setWindowTitle(title)
        self.show()

def main():
    app = QApplication(sys.argv)
    a = Master()
    sys.exit(app.exec_())

main()

# previous_course_selection = self.get_current_selection("course")
# if len(self.course.not_so_current_selection) == 2:
#     previous_course_selection = self.course.not_so_current_selection.pop(0)
#     for date in range(self.date.date_list.count()):
#         self.stored_info[previous_course_selection].list_data[self.date.date_list.takeItem(0).text()] = \
#             [self.chapter.chapter_list.takeItem(0).text() for item in range(self.chapter.chapter_list.count())]
# self.load_list(current_type, previous_course_selection)