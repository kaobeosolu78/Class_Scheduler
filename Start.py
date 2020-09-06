import __init__
import os, sys
sys.path.insert(0, os.path.abspath("."))
import datetime
import Upload
import pickle
# current chapter and current page

# gets a range of datetime vals from start->end
def date_range(start, end):
    date_list = [datetime.date.fromordinal(i) for i in range(start.toordinal(), end.toordinal())]
    return date_list

# loads pickled object
def load_obj(datatype):
    with open("{}".format(datatype) + '.pkl', 'rb') as f:
        return pickle.load(f)

# saves pickled object
def save_obj(name, data):
    pick_out = open(f"{name}.pkl", "wb")
    pickle.dump(data, pick_out, pickle.HIGHEST_PROTOCOL)
    pick_out.close()

class Chapter:
    def __init__(self, chapter, chapter_info):
        self.chapter_name = chapter
        self.exam_number, self.start_page, self.end_page = chapter_info
        self.urgency = 0

    def get_page_sum(self):
        return self.end_page-self.start_page

    def calculate_urgency(self, exam_page_sum, date_range_length):
        self.urgency = round((self.get_page_sum()/exam_page_sum)*date_range_length)

class Course:
    def __init__(self, name, start_page, exam_dates, chapters, cooldown, start_date=datetime.date.today()):
        # initialize vars
        self.name = name
        self.start_date = start_date  # datetime.date.today()
        self.start_page = start_page
        self.exam_dates = exam_dates
        self.chapter_info = {name: Chapter(name, info) for name, info in list(chapters.items()) if not info[2] < self.start_page}
        self.cooldown = cooldown
        self.exam_info = tuple({"Date Range": []} for _ in self.exam_dates)
        self.all_dates = date_range(self.start_date, self.exam_dates[-1])

        def calendar_generator(exam_num):
            for chapter_name, chapter in list(self.chapter_info.items()) :
                if chapter.exam_number == exam_num:
                    yield chapter_name

        self.calendar = tuple({chapter: [] for chapter in calendar_generator(exam_num)} for exam_num in range(len(exam_dates)))
        # one liner for lines 46-52
        # self.calendar = tuple({chapter: [] for chapter in (chapter_name for chapter_name, chapter in list(self.chapter_info.items()) if chapter.exam_number == exam_num)} for exam_num in range(len(exam_dates)))

        # call necessary methods
        self.get_exam_date_ranges()
        self.adjust_dates()
        self.add_pages()
        self.calculate_urgency()
        self.set_dates()
        self.finalize()
        # self.display()
        print()

    # creates a list of datetimes between each exam
    def get_exam_date_ranges(self):
        for exam_date_ind, exam in enumerate(self.exam_info):
            exam["Date Range"] = date_range(([self.start_date] + self.exam_dates)[exam_date_ind],
                                                  ([self.start_date] + self.exam_dates)[exam_date_ind+1])

    # removes the exam date from all date ranges and a variable number of dates after the exam
    def adjust_dates(self):  # improve
        for remove_date in [exam_date+datetime.timedelta(days=days_after_exam)
                for exam_date in self.exam_dates[1:] for days_after_exam in range(self.cooldown)]:
            for date in self.all_dates:
                if remove_date == date or date < self.start_date:
                    # if remove_date in self.all_dates:
                    del self.all_dates[self.all_dates.index(date)]
            for exam in self.exam_info:
                for date in exam["Date Range"]:
                    if remove_date == date or date < self.start_date:
                        del exam["Date Range"][exam["Date Range"].index(date)]

    def adjust_chapters(self):
        pass

    # calculate total pages per exam
    def add_pages(self):
        for exam_number, exam in enumerate(self.exam_info):
            for chapter_name, chapter in list(self.chapter_info.items()):
                if chapter.exam_number == exam_number:
                    exam["Total Pages"] = exam.get("Total Pages", 0) + chapter.get_page_sum()  # combine two loops

    # for each chapter, create a ratio [(pages in chapter/pages required for exam)*(total dates)] that will be used to
    # calculate how many days each chapter should be studied
    def calculate_urgency(self):
        for exam_number, exam in enumerate(self.exam_info):
            for chapter in list(self.chapter_info.values()):
                if chapter.exam_number == exam_number:
                    chapter.calculate_urgency(exam["Total Pages"], len(exam["Date Range"]))


        # test, temp = 0, ""
        # for ind in range(len(self.exam_date_ranges)):
        #     for chap in list(self.chapter_info.keys()):
        #         # calculate urgency ratio
        #         if self.chapter_info[chap][0] == ind:
        #             temp = chap
        #             self.chapter_info[chap].append(("Urgency", round((self.chapter_info[chap][3][1] / self.exam_info[ind][0][1]) * len(self.exam_date_ranges[ind]))))
        #             test += round((self.chapter_info[chap][3][1] / self.exam_info[ind][0][1]) * len(self.exam_date_ranges[ind]))
        #     # edge case, rounds differently if on the last date of the range
        #     if test > len(self.exam_date_ranges[ind]):
        #         self.chapter_info[temp][4] = ("Urgency",int((self.chapter_info[temp][3][1] / self.exam_info[ind][0][1]) * len(self.exam_date_ranges[ind])))

    # create a calendar and portion out the chapters
    def set_dates(self):
        date_total_index = 0
        for chapter in list(self.chapter_info.values()):
            pages = ()
            for day_ind, day in enumerate(range(chapter.urgency)):
                pages = (int(chapter.start_page+(day_ind)*(chapter.get_page_sum()/chapter.urgency)),
                          int(chapter.start_page+(day_ind+1)*(chapter.get_page_sum()/chapter.urgency)))
                self.calendar[chapter.exam_number][chapter.chapter_name].append((self.all_dates[date_total_index], pages))
                date_total_index += 1

    # add cal to google calendar
    def display(self):
        Upload.main("Add", self.calendar, self.exam_dates)


    # pickle out calendar
    def finalize(self):
        # calendars = load_obj("calendars")
        print("")
        # calendars[self.name] = self.calendar
        save_obj("calendar", self.calendar)


def main():
    test = Course("Physics", 750, [datetime.date(2020,6,4),datetime.date(2020,7,7),datetime.date(2020,7,28),datetime.date(2020,8,11)], {"Electrostatics":[0,651,675], "Electric Fields" : [0,676,708], "Electric Potential" : [0,709,736], "Capacitors" : [0,737,764], "Current and Resistance" : [1,765,794], "Direct Current" : [1,795,818], "Magnetism" : [1,819,844], "Magnetic Fields" : [1,845,874], "Electromagnetic Induction" : [1,875,906], "EM Oscillations" : [2,907,938], "Electromagnetic Waves" : [2,939,970], "Geometric Optics" : [2,971,1002], "Special Relativity" : [3,1072,1107]}, 2, datetime.date(2020, 5, 25))
    # test = Course("Orgo", [datetime.date(2020,6,30),datetime.date(2020,7,28)], {"Alcohols":[0,10,40], "Ketones":[0,41,73], "Aromatics":[0,74,102]}, 2)
    print(test.calendar)

if __name__ == "__main__":
    main()