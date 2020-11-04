import datetime
import operator
import re
import typing

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

    @classmethod
    def load(cls):
        result = requests.get(Timetable.URL_TIMETABLE)
        return cls._parse_html_timetable(result.text)

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
        self.date = datetime.date(day=int(split_date[0]),
                                  month=int(split_date[1]),
                                  year=int(split_date[2]))

    @classmethod
    def _parse_html_timetable(cls, html: str):
        def marge_timetables(*timetables):
            """Слияние 2 и более распиания"""
            marged_timetable = cls()
            for timetable in timetables:
                marged_timetable += timetable

            return marged_timetable


        soap = BeautifulSoup(html, "html.parser")

        soap_timetables = []
        for html_class in cls.HTML_CLASSES_TIMETABLE:
            soap_timetable = soap.find(class_=html_class)
            if soap_timetable is not None:
                soap_timetables.append(soap_timetable)

        timetables = list()
        for i in soap_timetables:
            i.find(class_='title').extract()
            timetable = cls._parse_text(i.get_text())
            timetables.append(timetable)

        return marge_timetables(*timetables)

    @classmethod
    def _parse_text(cls, text: str):
        def delete_info_text(lines: typing.List[str]) -> typing.List[str]:
            """Удаляет строки с дополнитльной информацией, которые идут перед расписанием, а так же разделители между
            расписанием групп."""
            timetable_lines = []
            is_began_timetable = False

            for line in lines:
                if re.match(r'^-+$', line):
                    is_began_timetable = True
                elif is_began_timetable:
                    timetable_lines.append(line)

            return timetable_lines

        tb = cls()
        lines = [s for s in text.splitlines() if s.strip() != '']

        # Дата находится в первой строке в формате
        # "Расписание 31.10.2020 Суббота (Заочное отделение)"
        tb._parse_date(lines.pop(0))
        timetable_lines = delete_info_text(lines)

        for line in timetable_lines:
            line = re.sub(r'\s{2,}', ' ', line)
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
