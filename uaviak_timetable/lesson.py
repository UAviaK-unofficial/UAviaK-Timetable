import re


class ParseLessonError(Exception):
    pass


class Lesson:
    ATTR = [
        'group',
        'number',
        'is_splitting',
        'cabinet',
        'teacher',
        'subject',
        'is_practice',
        'is_consultations'
    ]

    def __init__(
            self,
            group: str,
            number: int,
            is_splitting: bool,
            cabinet: str,
            teacher: str,
            subject: str,
            is_practice: bool,
            is_consultations: bool,
            is_exam: bool
    ):
        self.group = group
        self.number = number
        self.is_splitting = is_splitting
        self.cabinet = cabinet
        self.teacher = teacher
        self.subject = subject
        self.is_practice = is_practice
        self.is_consultations = is_consultations
        self.is_exam = is_exam

    @classmethod
    def parse_line(cls, line: str):
        # 17ам-1  1     Маст.Шакиров И.Г.       Производственная практика                Практика
        result = re.match(r'(\d{2}\S{1,4})\s+(\d)\s+(дрб)?\s+(\S{1,5})\s*(\S+\s\S\.\S\.)\s+(.+)', line)
        if not result:
            raise ParseLessonError('Error parse line lesson', line)
        re_groups = result.groups()

        return cls(
            group=re_groups[0],
            number=int(re_groups[1]),
            is_splitting=re_groups[2] is not None,
            cabinet=re_groups[3],
            teacher=re_groups[4],
            subject=re_groups[5].replace('Практика', '').replace('Консультация', '').replace('Консульт', '').replace(
                'Экзамен', '').strip(),
            is_practice=re_groups[5].find('Практика') != -1,
            is_consultations=re_groups[5].find('Консульт') != -1 or re_groups[5].find('Консультация') != -1,
            is_exam=re_groups[5].find('Экзамен') != -1
        )
