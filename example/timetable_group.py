#!/usr/bin/python3
from uaviak_timetable import Timetable
import sys

# Получаем номер группы
if len(sys.argv) < 2:
    group = input('Группа: ')
else:
    group = sys.argv[1]

# Инициализируем объект
table = Timetable.load()

# Ищем `Lesson` для группы `group`
finds_table = table.find(group=group)
# Сортируем по порядку
finds_table.sort('number')

# Выводим на экран
for lesson in finds_table:
    print(f'{lesson.number}) {lesson.subject}{" (Практика)" if lesson.is_practice else ""}')
print(table.date.strftime('%A %d.%m'))
