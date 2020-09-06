from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QFormLayout, QLineEdit, \
    QPushButton, QMainWindow, QAction, QListWidget, QErrorMessage
from Start import load_obj, save_obj, Course
import datetime
from operator import attrgetter
from PyQt5 import QtCore, QtWidgets
import sys
import abc
import time
# cheeeeck function calls on composition vs inheritance
# add decorator for setting current_type
# check out viability of descriptor implementation in some vars
# implement current_type = self.__class__.__name__[3:-1].lower()
# relearn args+kwargs
# yield from


def datetime_conversion(date_str):  # maybe add date list instead of manual input
    for month_format in ["%m", "%-m", "%B", "%b"]:  # also maybe remove seps and replace with /
        for day_format in ["%d", "%-d"]:
            for year_format in ["%y", "%Y", "%-y"]:
                for sep_format_1, sep_format_2 in zip([" ", "/", "-", " "],[", ", "/", "-", " "]):
                    try:
                        return datetime.datetime.strptime(date_str, f"{month_format}{sep_format_1}{day_format}{sep_format_2}{year_format}")
                    except:
                        pass


class CourseSchedule:
    def __init__(self, course_name, cooldown, start_page):
        self.course_name = course_name
        self.cooldown = cooldown  # get rid of this
        self.start_page = start_page
        self.exam_dates = []
        self.chapters = {}

    def course_loadable(self):
        return [self.course_name, self.cooldown, self.start_page]

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
        self.error = QtWidgets.QErrorMessage(self)
        self.error.setWindowModality(QtCore.Qt.WindowModal)

    def add_button(self, name, coords, layout, current_type):
        button = QPushButton(name.title())
        button.clicked.connect(lambda: getattr(self, name)(current_type))
        self.master.__dict__[layout].addWidget(button, coords[0], coords[1])

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
    def __init__(self, master):# fix
        super().__init__(master)


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


class Home_Screen(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.window = QWidget(self)
        self.setCentralWidget(self.window)

        self.grid = QGridLayout()
        self.calendar = load_obj("calendar")

        self.add_labels()
        self.display("Test")
        print()

    def add_menu(self):
        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")

        menu = QAction("Edit Courses", self)
        menu.triggered.connect(lambda: self.edit_info())
        filemenu.addAction(menu)

    def add_labels(self):
        for course_ind, course_name in enumerate(["Physics"]):
            chapter_ind = 0
            label = QLabel(f"----{course_name}----")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.grid.addWidget(label, 0, course_ind)
            chapters, exams = self.get_active_info(self.calendar)
            for chapter_name, dates in list(chapters.items()):
                chapter_ind += 1
                label = QLabel(chapter_name)
                label.setAlignment(QtCore.Qt.AlignCenter)
                self.grid.addWidget(label, chapter_ind, course_ind)
                for date in dates:
                    chapter_ind += 1
                    label = QLabel(str(f"{date}"))
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    self.grid.addWidget(label, chapter_ind, course_ind)

    def get_active_info(self, course_calendar):
        lookahead = 0
        current_chapters = {}
        current_exams = []
        for exam_number, exam in enumerate(list(course_calendar)):
            for chapter_name, chapter in list(exam.items()):
                for date_ind in range(len(chapter)):
                    if datetime.date(2020, 5, 20) <= chapter[date_ind]:
                        if exam_number not in current_exams: current_exams.append(exam_number)
                        current_chapters[chapter_name] = current_chapters.get(chapter_name, []) + [chapter[date_ind]]
                        lookahead += 1
                        if lookahead == 5:
                            return (current_chapters, current_exams)

    def edit_info(self):
        pass


    def display(self, title, x_dim=500, y_dim=400):
        self.window.setLayout(self.grid)
        self.setGeometry(1300, 300, x_dim, y_dim)
        self.setWindowTitle(title)
        self.show()

    # def check_past_exam(self):
    #     passed_exams = {}
    #     for class_ in list(self.raw_data.keys()):
    #         passed_exams[class_] = []
    #         for ind,exam in enumerate(self.raw_data[course_]["Exam Dates"]):
    #             if datetime.datetime.today() > exam+datetime.timedelta(days=7):
    #                 passed_exams[class_].append((exam,ind))




class AddCourses(GuiFunctions):
    def __init__(self, master):
        super().__init__(master)

        self.course_input = [QLineEdit() for _ in range(3)]

        self.add_layouts("course_grid", 50)
        self.add_labels(["Course \nName:", "Rest Days \nAfter Exam:", "Start Page:"])
        self.add_inputs("course")
        self.add_button("add", (3, 0), "left_grid", "course")  # add loop
        self.add_button("delete", (3, 1), "left_grid", "course")
        self.add_listbox("course")

    def store_info(self):
        course_info = super().store_info("course")
        self.master.stored_info[course_info[0]] = CourseSchedule(course_info[0], course_info[1], course_info[2])  # add error dialog or descriptor

    def load_info(self):
        self.set_input_text(self.master.stored_info[self.master.get_current_selection("course")].course_loadable(), "course")
        self.master.save_list(True)

    def delete(self, *args):
        del self.master.stored_info[self.master.get_current_selection("course")]
        super().delete(["course", "date", "chapter"])


class AddDates(GuiFunctions):

    def __init__(self, master):
        super().__init__(master)

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
        super().__init__(master)

        self.chapter_input = [QLineEdit() for _ in range(3)]

        self.add_layouts("chapter_grid", 27)
        self.add_labels(["Chapter \nName:", "First Page:", "Last Page"])
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
        del self.master.stored_info[self.master.get_current_selection("course")].chapters[self.master.get_current_selection("chapter")]  # add error dialog for no selection
        super().delete(["chapter"])

    def submit(self, current_type):
        for course, sched in list(self.master.stored_info.items()):
            Course(course, datetime_conversion(sched.start_page), [datetime_conversion(date) for date in sched.exam_dates],
                  {name: [int(val) for val in info] for name, info in sched.chapters.items()}, int(sched.cooldown))


class Master(QMainWindow):
    def __init__(self):
        super().__init__()
        self.add_window()
        self.add_all_layouts()

        self.stored_info = {}
        self.course = AddCourses(self)
        self.date = AddDates(self)
        self.chapter = AddChapters(self)
        self.display("Schedule")


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



