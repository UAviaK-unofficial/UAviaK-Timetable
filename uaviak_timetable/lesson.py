import re
from typing import List

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
            is_collage: bool,
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
        self.is_collage = is_collage
        self.cabinet = cabinet
        self.teacher = teacher
        self.subject = subject
        self.is_practice = is_practice
        self.is_consultations = is_consultations
        self.is_exam = is_exam

    @classmethod
    def parse_line(cls, line: str):
        def is_exist_element(elements: List[str], index: int, s: str) -> bool:
            """Существует ли элемент в строке, если да, то возвращает его и удаляет из списка.

            :param elements: Список элементов для поиска.
            :param index: Индекс сравниваемого элемента.
            :param s: Шаблон для поиска.
            :return: True - если совпадает, иначе False
            """
            if elements[index] == s:
                del elements[index]
                return True

            return False
        # Разъединяем слипшиеся номер кабинета и ФИО.
        # Например, "407*кКожевникова" -> "407*к Кожевникова"
        line = line.replace('*к', '*к ')

        line_split = line.split()

        group = line_split.pop(0)
        number = line_split.pop(0)
        is_splitting = is_exist_element(line_split, 0, 'дрб')
        is_collage = is_exist_element(line_split, 0, '(колледж)')
        cabinet = line_split.pop(0)

        teacher = ' '.join(line_split[0:2])
        del line_split[0:2]

        is_practice = is_exist_element(line_split, -1, 'Практика')
        is_consultations = is_exist_element(line_split, -1, 'Консульт') or \
                           is_exist_element(line_split, -1, 'Консультация')
        is_exam = is_exist_element(line_split, -1, 'Экзамен')
        subject = ' '.join(line_split)

        return cls(
            group=group,
            number=int(number),
            is_splitting=is_splitting,
            is_collage=is_collage,
            cabinet=cabinet,
            teacher=teacher,
            subject=subject,
            is_practice=is_practice,
            is_consultations=is_consultations,
            is_exam=is_exam
        )


        # def subject_proc(subject: str):
        #     types_lesson = {
        #         'Практика': False,
        #         'Консультация': False,
        #         'Консульт': False,
        #         'Экзамен': False
        #     }
        #
        #     for type_ in types_lesson:
        #         if subject.find(type_) != -1:
        #             types_lesson[type_] = True
        #             subject = subject.replace(type_, '').strip()
        #
        #     return types_lesson['Практика'], \
        #            types_lesson['Консультация'] or types_lesson['Консультация'], \
        #            types_lesson['Экзамен'], \
        #            subject
        #
        # result = re.match(r'(\d{2}\S{1,4})\s(\d)\s(дрб)?\s?(\S{1,5})\s?(\S+\s\S\.\S\.)\s+(.+)', line)
        # if not result:
        #     raise ParseLessonError('Error parse line lesson', line)
        # re_groups = result.groups()
        #
        # is_practice, is_consultations, is_exam, subject = subject_proc(re_groups[5])
        # return cls(
        #     group=re_groups[0],
        #     number=int(re_groups[1]),
        #     is_splitting=re_groups[2] is not None,
        #     cabinet=re_groups[3],
        #     teacher=re_groups[4],
        #     subject=subject,
        #     is_practice=is_practice,
        #     is_consultations=is_consultations,
        #     is_exam=is_exam
        # )

    def __repr__(self):
        return f'<{self.group} {self.subject}>'
