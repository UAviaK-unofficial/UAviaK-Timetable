import datetime
import operator
import re

import requests
from bs4 import BeautifulSoup

from . import Lesson


class Timetable:
    URL_TIMETABLE = 'http://www.uaviak.ru/pages/raspisanie-/'
    HTML_CLASSES_TIMETABLE = [
        'scrolling-text pos1',
        'scrolling-text pos2'
    ]

    def __init__(self):
        self.lessons = []
        self.date = None

    def find(self, **kwargs):
        tb = self.__class__()
        tb.date = self.date

        for lesson in self.lessons:
            for attr in kwargs:
                if getattr(lesson, attr) == kwargs[attr]:
                    tb.append_lesson(lesson)

        return tb

    def sort(self, attr: str = 'number', reverse: bool = False):
        self.lessons.sort(key=operator.attrgetter(attr), reverse=reverse)

    def list(self, fild):
        if not fild in Lesson.ATTR:
            raise ValueError('Not found fild')

        value_filds = set()
        for lesson in self.lessons:
            value_filds.add(getattr(lesson, fild))

        return list(value_filds)

    def append_lesson(self, lesson: Lesson or str):
        if isinstance(lesson, Lesson):
            self.lessons.append(lesson)
        elif isinstance(lesson, str):
            self.lessons.append(Lesson.parse_line(lesson))
        else:
            raise TypeError()

    def _parse_date(self, str_with_date: str or list):
        if isinstance(str_with_date, str):
            str_with_date = str_with_date.split()

        # Строка с датой может быть 2 форматов, с предлогом "на", пример
        #     Расписание на 01.01.1970
        # и без
        #     Расписание 01.01.1970
        if 'на' in str_with_date:
            str_with_date.remove('на')

        split_date = str_with_date[1].split('.')
        self.date = datetime.date(day=int(split_date[0]), month=int(split_date[1]), year=int(split_date[2]))

    @classmethod
    def load(cls):
        result = requests.get(Timetable.URL_TIMETABLE)

        soap = BeautifulSoup(result.text, "html.parser")

        soap_timetables = []
        for html_class in cls.HTML_CLASSES_TIMETABLE:
            soap_timetables.append(soap.find(class_=html_class))

        timetables = list()
        for i in soap_timetables:
            i.find(class_='title').extract()
            timetable = cls.__parse_text(i.get_text())
            timetables.append(timetable)

        return timetables[0] + timetables[1]

    @classmethod
    def is_lesson_line(cls, line: str):
        return len(line) != 0 and \
               line[0][:2].isnumeric() and \
               line[0][-1] != ',' and \
               not line[-1].isnumeric()

    @classmethod
    def __parse_text(cls, text: str):
        tb = cls()
        lines = text.splitlines()

        for line in lines:
            # Удаляем лишние пробельные символы
            line = line.strip()
            line = re.sub(r'\s{2,}', ' ', line)

            split_line = line.split()
            if len(split_line) > 0:
                if not tb.date and split_line[0] == 'Расписание':
                    tb._parse_date(split_line)
                elif cls.is_lesson_line(line):
                    tb.append_lesson(line)

        return tb

    def __getitem__(self, item):
        return self.lessons[item]

    def __len__(self):
        return len(self.lessons)

    def __str__(self):
        return str(self.lessons)

    def __repr__(self):
        return str(self.lessons)

    def __add__(self, other: 'Timetable'):
        def _is_new_date(date):
            return self.date is None or self.date < date

        sum_timetable = self.__class__()

        sum_timetable.lessons += self.lessons
        sum_timetable.lessons += other.lessons

        if _is_new_date(other.date):
            sum_timetable.date = other.date
        else:
            sum_timetable.date = self.date

        return sum_timetable
