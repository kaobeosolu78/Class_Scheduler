import __init__
import os, sys
sys.path.insert(0, os.path.abspath("."))
import datetime
# import Upload
import pickle

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

class Course:
    def __init__(self, name, exam_dates, chapters, cooldown):
        # initialize vars
        self.name = name
        self.exam_dates = exam_dates
        self.chapter_info = chapters
        self.cooldown = cooldown
        self.exam_info = {}
        self.total_page_num = 0
        self.exam_date_ranges = []
        self.all_dates = date_range(self.exam_dates[0], self.exam_dates[len(self.exam_dates)-1])
        self.calendar = {}

        # call necessary methods
        self.get_page_nums()
        self.get_dates()
        self.adj_dates()
        self.add_pages()
        self.calc_urgency()
        self.set_dates()
        self.finalize()
        self.display()

    # gets difference of input pages to find page num for each chapter
    def get_page_nums(self):
        for chap in list(self.chapter_info.keys()):
            self.chapter_info[chap].append(("Number of Pages", self.chapter_info[chap][2]-self.chapter_info[chap][1]))
            # also gets total number of pages
            self.total_page_num += self.chapter_info[chap][2]-self.chapter_info[chap][1]

    # creates a list of datetimes between each exam
    def get_dates(self):
        for k in range(len(self.exam_dates)-1):
            self.exam_date_ranges.append((date_range(self.exam_dates[k], self.exam_dates[k+1])))

    # removes the exam date from all date ranges and a variable number of dates after the exam
    def adj_dates(self):
        for k in range(self.cooldown):
            for date_ in [ex+datetime.timedelta(days=k) for ex in self.exam_dates[1:]]:
                if date_ in self.all_dates:
                    del self.all_dates[self.all_dates.index(date_)]
                for j in range(len(self.exam_date_ranges)):
                    if date_ in self.exam_date_ranges[j]:
                        del self.exam_date_ranges[j][self.exam_date_ranges[j].index(date_)]

    # calculate total pages per exam
    def add_pages(self):
        ind = 0
        while ind != len(self.exam_date_ranges):
            for chap in list(self.chapter_info.keys()):
                if ind == self.chapter_info[chap][0]:
                    self.exam_info.get(ind, [("Total Pages", 0)])
                    self.exam_info[ind][0] = ("Total Pages", self.exam_info[ind][0][1] + self.chapter_info[chap][3][1])
            ind += 1

    # for each chapter, create a ratio [(pages in chapter/pages requred for exam)*(total dates)] that will be used to
    # calculate how many days each chapter should be studied
    def calc_urgency(self):
        test, temp = 0, ""
        for ind in range(len(self.exam_date_ranges)):
            for chap in list(self.chapter_info.keys()):
                # calculate urgency ratio
                if self.chapter_info[chap][0] == ind:
                    temp = chap
                    self.chapter_info[chap].append(("Urgency", round((self.chapter_info[chap][3][1] / self.exam_info[ind][0][1]) * len(self.exam_date_ranges[ind]))))
                    test += round((self.chapter_info[chap][3][1] / self.exam_info[ind][0][1]) * len(self.exam_date_ranges[ind]))
            # edge case, rounds differently if on the last date of the range
            if test > len(self.exam_date_ranges[ind]):
                self.chapter_info[temp][4] = ("Urgency",int((self.chapter_info[temp][3][1] / self.exam_info[ind][0][1]) * len(self.exam_date_ranges[ind])))

    # create a calendar and portion out the chapters
    def set_dates(self):
        temp = self.all_dates
        count = 0
        chaps = list(self.chapter_info.keys())
        for chap in chaps:
            self.calendar.get(self.chapter_info[chap][0], {})
            self.calendar[self.chapter_info[chap][0]][chap] = []
            while count != self.chapter_info[chap][4][1]:
                self.calendar[self.chapter_info[chap][0]][chap].append(temp.pop(0))
                count+=1
            if temp != [] and chaps.index(chap) != len(chaps) and self.chapter_info[chap][0] != self.chapter_info[chaps[chaps.index(chap)+1]][0] and temp[0] < self.exam_dates[self.chapter_info[chap][0]+1]:
                self.calendar[self.chapter_info[chap][0]][chap].append(temp.pop(0))
            count = 0

    # add cal to google calendar
    def display(self):
        Upload.main("Add" ,self)

    print()
    # pickle out calendar
    def finalize(self):
        calendars = load_obj("calendars")
        calendars[self.name] = self.calendar
        pick_out = open("calendars.pkl", "wb")
        pickle.dump(calendars, pick_out, pickle.HIGHEST_PROTOCOL)
        pick_out.close()

def main():
    # test = Course("Physics", [datetime.date(2020,6,29),datetime.date(2020,6,4),datetime.date(2020,7,7),datetime.date(2020,7,28),datetime.date(2020,8,11)], {"Electrostatics":[0,651,675], "Electric Fields" : [0,676,708], "Electric Potential" : [0,709,736], "Capacitors" : [0,737,764], "Current and Resistance" : [1,765,794], "Direct Current" : [1,795,818], "Magnetism" : [1,819,844], "Magnetic Fields" : [1,845,874], "Electromagnetic Induction" : [1,875,906], "EM Oscillations" : [2,907,938], "Electromagnetic Waves" : [2,939,970], "Geometric Optics" : [2,971,1002], "Special Relativity" : [3,1072,1107]}, 2)
    test = Course("Orgo", [datetime.date(2020,6,30),datetime.date(2020,7,28)], {"Alcohols":[0,10,40], "Ketones":[0,41,73], "Aromatics":[0,74,102]}, 2)
    print(test.calendar)

if __name__ == "__main__":
    main()