from . import Lesson

import requests
import operator
from bs4 import BeautifulSoup


class Timetable:
    URL_TIMETABLE = 'http://www.uaviak.ru/pages/raspisanie-/'

    def __init__(self):
        self.lessons = []

    def find(self, **kwargs):
        tb = Timetable()

        for lesson in self.lessons:
            for attr in kwargs:
                if getattr(lesson, attr) == kwargs[attr]:
                    tb.append_lesson(lesson)

        return tb

    def sort(self, attr: str = 'number', reverse: bool = False):
        self.lessons.sort(key=operator.attrgetter(attr), reverse=reverse)

    def append_lesson(self, lesson: Lesson or str):
        if isinstance(lesson, Lesson):
            self.lessons.append(lesson)
        elif isinstance(lesson, str):
            self.lessons.append(Lesson.parse_line(lesson))
        else:
            raise TypeError()

    @classmethod
    def load(cls):
        result = requests.get(Timetable.URL_TIMETABLE)

        soap = BeautifulSoup(result.text, "html.parser")
        soap_timetable = soap.find_all(class_='scrolling-text')[1:]

        table_text = ''
        for i in soap_timetable:
            i.find(class_='title').extract()
            table_text += i.get_text()

        return cls.__parse_text(table_text)

    @classmethod
    def __parse_text(cls, text: str):
        tb = cls()
        lines = text.splitlines()

        for line in lines:
            if len(line) == 88 and line != ('-' * 88):
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