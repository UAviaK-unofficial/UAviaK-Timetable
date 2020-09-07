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
        def subject_proc(subject: str):
            types_lesson = {
                'Практика': False,
                'Консультация': False,
                'Консульт': False,
                'Экзамен': False
            }

            for type_ in types_lesson:
                if subject.find(type_) != -1:
                    types_lesson[type_] = True
                    subject = subject.replace(type_, '').strip()

            return types_lesson['Практика'], \
                   types_lesson['Консультация'] or types_lesson['Консультация'], \
                   types_lesson['Экзамен'], \
                   subject

        result = re.match(r'(\d{2}\S{1,4})\s(\d)\s(дрб)?\s?(\S{1,5})\s?(\S+\s\S\.\S\.)\s+(.+)', line)
        if not result:
            raise ParseLessonError('Error parse line lesson', line)
        re_groups = result.groups()

        is_practice, is_consultations, is_exam, subject = subject_proc(re_groups[5])
        return cls(
            group=re_groups[0],
            number=int(re_groups[1]),
            is_splitting=re_groups[2] is not None,
            cabinet=re_groups[3],
            teacher=re_groups[4],
            subject=subject,
            is_practice=is_practice,
            is_consultations=is_consultations,
            is_exam=is_exam
        )
