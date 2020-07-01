# input: course-chapters-pages-exams

# output: when to study/practice
import __init__
import os, sys
sys.path.insert(0, os.path.abspath("."))
import datetime
import Upload
from decimal import *
import pickle

def date_range(start, end):
    # date_list = [start - datetime.timedelta(days=x) for x in range((end-start).days)]
    date_list = [datetime.date.fromordinal(i) for i in range(start.toordinal(), end.toordinal())]
    return date_list

def load_obj(datatype):
    with open("{}".format(datatype) + '.pkl', 'rb') as f:
        return pickle.load(f)


class Course:
    def __init__(self, name, exam_dates, chapters, cooldown):
        self.name = name
        self.exam_dates = exam_dates
        self.chapter_info = chapters
        self.cooldown = cooldown
        self.exam_info = {}
        self.total_page_num = 0
        self.exam_date_ranges = []
        self.all_dates = date_range(self.exam_dates[0], self.exam_dates[len(self.exam_dates)-1])
        self.calendar = {}

        self.get_page_nums()
        self.get_dates()
        self.adj_dates()
        self.add_pages()
        self.calc_urgency()
        self.set_dates()
        self.finalize()
        self.display()

    def get_page_nums(self):
        for chap in list(self.chapter_info.keys()):
            self.chapter_info[chap].append(("Number of Pages", self.chapter_info[chap][2]-self.chapter_info[chap][1]))
            self.total_page_num += self.chapter_info[chap][2]-self.chapter_info[chap][1]

    def get_dates(self):
        for k in range(len(self.exam_dates)-1):
            self.exam_date_ranges.append((date_range(self.exam_dates[k], self.exam_dates[k+1])))

    def adj_dates(self):
        for k in range(self.cooldown):
            for date_ in [ex+datetime.timedelta(days=k) for ex in self.exam_dates[1:]]:
                if date_ in self.all_dates:
                    del self.all_dates[self.all_dates.index(date_)]
                for j in range(len(self.exam_date_ranges)):
                    if date_ in self.exam_date_ranges[j]:
                        del self.exam_date_ranges[j][self.exam_date_ranges[j].index(date_)]
        print()
    def add_pages(self):
        ind = 0
        while ind != len(self.exam_date_ranges):
            for chap in list(self.chapter_info.keys()):
                if ind == self.chapter_info[chap][0]:
                    try:
                        self.exam_info[ind]
                    except:
                        self.exam_info[ind] = [("Total Pages", 0)]
                    self.exam_info[ind][0] = ("Total Pages", self.exam_info[ind][0][1] + self.chapter_info[chap][3][1])
            ind += 1

    def calc_urgency(self):
        test, temp = 0, ""
        for ind in range(len(self.exam_date_ranges)):
            for chap in list(self.chapter_info.keys()):
                if self.chapter_info[chap][0] == ind:
                    temp = chap
                    self.chapter_info[chap].append(("Urgency", round((self.chapter_info[chap][3][1] / self.exam_info[ind][0][1]) * len(self.exam_date_ranges[ind]))))
                    test += round((self.chapter_info[chap][3][1] / self.exam_info[ind][0][1]) * len(self.exam_date_ranges[ind]))
            if test > len(self.exam_date_ranges[ind]):
                self.chapter_info[temp][4] = ("Urgency",int((self.chapter_info[temp][3][1] / self.exam_info[ind][0][1]) * len(self.exam_date_ranges[ind])))

    def set_dates(self):
        temp = self.all_dates
        count = 0
        chaps = list(self.chapter_info.keys())
        for chap in chaps:
            try:
                self.calendar[self.chapter_info[chap][0]]
            except:
                self.calendar[self.chapter_info[chap][0]] = {}
            self.calendar[self.chapter_info[chap][0]][chap] = []
            while count != self.chapter_info[chap][4][1]:
                self.calendar[self.chapter_info[chap][0]][chap].append(temp.pop(0))
                count+=1
            if temp != [] and chaps.index(chap) != len(chaps) and self.chapter_info[chap][0] != self.chapter_info[chaps[chaps.index(chap)+1]][0] and temp[0] < self.exam_dates[self.chapter_info[chap][0]+1]:
                self.calendar[self.chapter_info[chap][0]][chap].append(temp.pop(0))
            count = 0

    def display(self):
        Upload.main("Add" ,self)

    def finalize(self):
        calendars = load_obj("calendars")
        calendars[self.name] = self.calendar
        pick_out = open("calendars.pkl", "wb")
        pickle.dump(calendars, pick_out, pickle.HIGHEST_PROTOCOL)
        pick_out.close()

class process:
    def __init__(self, courses=[]):
        self.master_courses = courses

    def add_course(self, new_course):
        self.master_courses.append(new_course)
        return


def main():
    # test = Course("Physics", [datetime.date(2020,6,29),datetime.date(2020,6,4),datetime.date(2020,7,7),datetime.date(2020,7,28),datetime.date(2020,8,11)], {"Electrostatics":[0,651,675], "Electric Fields" : [0,676,708], "Electric Potential" : [0,709,736], "Capacitors" : [0,737,764], "Current and Resistance" : [1,765,794], "Direct Current" : [1,795,818], "Magnetism" : [1,819,844], "Magnetic Fields" : [1,845,874], "Electromagnetic Induction" : [1,875,906], "EM Oscillations" : [2,907,938], "Electromagnetic Waves" : [2,939,970], "Geometric Optics" : [2,971,1002], "Special Relativity" : [3,1072,1107]}, 2)
    test = Course("Orgo", [datetime.date(2020,6,30),datetime.date(2020,7,28)], {"Alcohols":[0,10,40], "Ketones":[0,41,73], "Aromatics":[0,74,102]}, 2)
    print(test.calendar)

if __name__ == "__main__":
    main()