# Конфигурационное управление
## Домашнее задание №1. Вариант 22:
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу 
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. 
Эмулятор должен запускаться из реальной командной строки, а файл с 
виртуальной файловой системой не нужно распаковывать у пользователя. 
Эмулятор принимает образ виртуальной файловой системы в виде файла формата 
zip. Эмулятор должен работать в режиме CLI. 
Ключами командной строки задаются: 
1. Путь к архиву виртуальной файловой системы.
2. Путь к стартовому скрипту. 

Стартовый скрипт служит для начального выполнения заданного списка 
команд из файла. 
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также 
следующие команды: 
1. touch. 
2. mv. 
Все функции эмулятора должны быть покрыты тестами, а для каждой из 
поддерживаемых команд необходимо написать 2 теста.

# Необходимые библиотеки
Для запуска программы, тестирующей функции, необходима библиотека `pytest`
Установка:
```BASH
pip install -U pytest
```

# Запуск
Для запуска проекта необходимо иметь сам проект (например, путем клонирования репозитория).
Перед запуском убедитесь в наличии необходимых библиотек

Запуск эмулятора:
```BASH
python main.py <path/to/vfs.zip> <path/to/start.sh>
```
Запуск программы, тестирующей функции
```BASH
pytest -v test_conf.py
```

# Команды
`ls <path>` - Список файлов и директорий указанной/текущей директории

`cd <path>` - Перемещение в указанную директорию

`touch <path/filename>` - Создание файла в указанной/текущей директории

`mv <path/filename> <new_path>` - Перемещение файла/директории из указанной/текущей директории в указанную/текущую директорию

`exit` - Выход из эмулятора

# Тестирование команд
## ls
![img.png](png/ls.png)
## cd
![img.png](png/cd.png)
## touch
![img.png](png/touch.png)
## mv
![img.png](png/mv.png)
## exit
![img_1.png](png/exit.png)
## pytest
![img.png](png/test_conf.png)
