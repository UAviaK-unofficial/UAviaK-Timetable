# Библиотека для получения расписания УАвиК'a
Библиотека позволяет удобно получать расписание с сайта
[Ульяновского авиационного колледжа](http://www.uaviak.ru/pages/raspisanie-/#pos1)

## Установка
1. Скачиваем библиотеку
    ```shell script
    git clone https://github.com/UAviaK-unofficial/UAviaK-Timetable.git
    cd UAviaK-Timetable
    ```
1. Устанавливаем
    ```shell script
    python setup.py install
    ```
## Зависимости
 - [requests](https://pypi.org/project/requests/)
 - [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

## Начало работы
Создаем объект и получаем расписание
```python
from uaviak_timetable import Timetable
tt = Timetable.load()
```
---
Получаем расписание одной группы и сортируем по номеру урока
```python
from uaviak_timetable import Timetable
tt = Timetable.load()

tt_group = tt.find(group='19ис-1')
tt_group.sort('number')
```
---
Выборка по номеру пары и сортировка по группе
```python
from uaviak_timetable import Timetable
tt = Timetable.load()

tt_number = tt.find(number=1)
tt_number.sort('group')
```

