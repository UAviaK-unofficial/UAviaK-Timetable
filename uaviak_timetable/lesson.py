class Lesson:
    def __init__(
            self,
            group: str,
            number: int,
            is_splitting: bool,
            cabinet: str,
            teacher: str,
            subject: str,
            is_practice: bool,
            is_consultations: bool
    ):
        self.group = group
        self.number = number
        self.is_splitting = is_splitting
        self.cabinet = cabinet
        self.teacher = teacher
        self.subject = subject
        self.is_practice = is_practice
        self.is_consultations = is_consultations

    @classmethod
    def parse_line(cls, line: str):
        return cls(
            group=line[:6].strip(),
            number=int(line[8]),
            is_splitting=line[10:13] == 'дрб',
            cabinet=line[14:19].strip(),
            teacher=line[19:37].strip(),
            subject=line[38:].replace('Практика', '').replace('Консульт', '').strip(),
            is_practice=line[79:].strip() == 'Практика',
            is_consultations=line[79:].strip() == 'Консульт'
        )