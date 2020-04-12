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
    def parse_line(cls, line: str or list):
        if isinstance(line, str):
            line = line.split()

        is_practice = line[-1] == 'Практика'
        is_consultations = line[-1] == 'Консульт' or line[-1] == 'Консультация'
        is_exam = line[-1] == 'Экзамен'
        if is_practice or is_consultations or is_exam:
            del line[-1]

        group = line[0]
        number = int(line[1])

        is_splitting = line[2] == 'дрб'
        if is_splitting:
            del line[2]

        cabinet = line[2]
        if line[3][1::2] == '..':
            cabinet = ''
            line.insert(2, '')

        teacher = f'{line[3]} {line[4]}'
        subject = ' '.join(line[5:])

        return cls(
            group=group,
            number=number,
            is_splitting=is_splitting,
            cabinet=cabinet,
            teacher=teacher,
            subject=subject,
            is_practice=is_practice,
            is_consultations=is_consultations,
            is_exam=is_exam
        )
