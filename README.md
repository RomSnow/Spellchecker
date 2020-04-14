# Спеллчекер
Автор: Ивашкин Роман (ivashkin.roma2001@yandex.ru)

Описание
-------------------------
Программа для нахождения ошибок и опечатков в текстовом файле.

Требования
------------------------
* Python 3

Состав
------------------------
* Консольная версия `cmain.py`
* Рабочие файлы программы `Spellchecker/`
* Словари `Dictionaries/`
* Справка по консольной версии `chelp.txt`
* README.md

Консольная версия
-----------------------
Запуск программы: `./cmain.py [OPTION]... [FILE]`

#### OPTIONS
* Справка: `-h`, `--help`
* Добавление слов в словарь: `--add [WORDS]`
* Запуск в _Speed_mode_(быстрее, но менее точно): `-s`, `--speed`

#### Пример работы программы
Исходный текст:
  > Я помню чутное мгновение,
  
  > Предомной евилась ты.
  
  > Как мемлетное ведение,
  
  > Как гений чистой красоты
  
Вывод программы:
  > чутное ?--> (четное чудное чумное чуткое чётное) на строке 1
  
  > предомной ?--> (предурной препоной преумной придонной проломной) на строке 2
  
  > евилась ?--> (вилась ежилась свилась явилась) на строке 2
  
  > мемлетное ?--> (медленное меленное мимолетное нелетное) на строке 3
